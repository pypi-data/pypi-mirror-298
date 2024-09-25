###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Integration with external services for Production Management System"""

from __future__ import annotations

import asyncio
import base64
import binascii
import hashlib
import json
import os
import re
import time
from abc import ABCMeta
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import gitlab
import prompt_toolkit
import requests
import yaml
from bs4 import BeautifulSoup
from rich.progress import Progress, MofNCompleteColumn, TimeElapsedColumn

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

CACHE_DIR = Path.home() / ".cache" / "dirac" / "production-management"
METADATA_HEADER = "<details><summary>Prod Metadata</summary>"
RE_METADATA = re.compile(r"(<details>\n?<summary>Prod Metadata</summary>\n\n```json\n)([^`]+)(\n```\n\n</details>)")
PROGRESS_COLUMNS = [MofNCompleteColumn(), *Progress.get_default_columns(), TimeElapsedColumn()]


class RepoIssue:
    def __init__(self, issue: gitlab.v4.objects.ProjectIssue):
        self.issue = issue
        self.run_yaml_blob, self.request_yaml_blob = self._extract_request(self.issue)
        self.run_yaml = self._parse_run_yaml_blob(self.run_yaml_blob)
        self.request_yaml = self._parse_request_yaml_blob(self.request_yaml_blob)
        self._extract_metadata()

    def __repr__(self):
        return f"RepoIssue({self.url})"

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, RepoIssue):
            return False
        return self.url == o.issue.attributes["web_url"]

    @property
    def state(self):
        matched = [k for k in self.labels if k.startswith("state::")]
        if len(matched) != 1:
            raise NotImplementedError(self, matched)
        return matched[0].split("::")[1]

    @property
    def url(self):
        return self.issue.attributes["web_url"]

    @property
    def labels(self):
        return self.issue.labels

    @property
    def discussions(self):
        return self.issue.discussions

    @property
    def all_transform_ids(self):
        ids = []
        for request_meta in self.metadata.get("requests", {}).values():
            ids.extend(request_meta["transform_ids"])
            ids.append(request_meta["removal"])
            ids.append(request_meta["replication"])
        return ids

    @staticmethod
    def _extract_request(issue):
        issue_url = issue.attributes["web_url"]
        run_yaml_blob = None
        request_yaml_blob = None
        for lang, blob in re.findall("```([^`\n]*)\n([^`]+)```", issue.description):
            lang = lang.strip().lower()
            if lang and lang != "yaml":
                continue
            loaded = yaml.safe_load(blob)
            if isinstance(loaded, dict):
                if run_yaml_blob is not None:
                    raise NotImplementedError(issue_url)
                run_yaml_blob = blob
                continue
            if isinstance(loaded, list):
                if request_yaml_blob is not None:
                    raise NotImplementedError(issue_url)
                request_yaml_blob = blob
                continue
            raise NotImplementedError(issue_url)

        if run_yaml_blob is None or request_yaml_blob is None:
            raise NotImplementedError(issue_url)

        return run_yaml_blob, request_yaml_blob

    @staticmethod
    def _parse_run_yaml_blob(run_yaml_blob):
        run_yaml = yaml.safe_load(run_yaml_blob)
        if set(run_yaml) != {"start_run", "end_run", "concurrent"}:
            raise NotImplementedError()
        if run_yaml["concurrent"]:
            if run_yaml["start_run"] is None or not isinstance(run_yaml["start_run"], int):
                raise NotImplementedError()
            if run_yaml["end_run"] is None or not isinstance(run_yaml["end_run"], int):
                raise NotImplementedError()
        if not isinstance(run_yaml["concurrent"], bool):
            raise NotImplementedError()
        return run_yaml

    @staticmethod
    def _parse_request_yaml_blob(request_yaml_blob):
        request_yaml = yaml.safe_load(request_yaml_blob)
        if len(request_yaml) != 1:
            raise NotImplementedError()
        request_yaml[0].pop("author", None)
        return request_yaml[0]

    def _extract_metadata(self):
        if self.issue.description.count("Prod Metadata") > 1:
            raise NotImplementedError(self.issue.attributes["web_url"])
        if METADATA_HEADER not in self.issue.description:
            self.issue.description += f"\n\n{METADATA_HEADER}\n\n```json\n{{}}\n```\n\n</details>"
        self.metadata = json.loads(RE_METADATA.search(self.issue.description).group(2))
        self.metadata.setdefault("validations", {})

    def update_metadata(self):
        self.issue.description, n = RE_METADATA.subn(
            rf"\1{json.dumps(self.metadata, indent=4)}\3",
            self.issue.description,
        )
        if n != 1:
            raise NotImplementedError(self)
        self.issue.save()


class DeviceFlowCredentials(metaclass=ABCMeta):
    sso_name: str
    use_pkce: bool

    def __init__(self, client_id, *, client_secret=None, scope=None, token_endpoint=None, device_flow_endpoint=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.device_flow_endpoint = device_flow_endpoint
        self.scope = scope
        self.refresh_token = None
        if self.cache_path.exists():
            cache = json.loads(self.cache_path.read_text())
            self.refresh_token = cache["refresh_token"]
            self.refresh_token_expires_at = cache["refresh_token_expires_at"]
        self.do_token_refresh()

    @property
    def cache_path(self):
        return CACHE_DIR / f"{self.client_id}.json"

    @property
    def access_token(self):
        if self.access_token_expires_at < time.time() + 60:
            self.do_token_refresh()
        return self._access_token

    def update_access_token(self, token_response):
        self._access_token = token_response["access_token"]
        self.access_token_expires_at = time.time() + token_response["expires_in"]

    def update_refresh_token(self, token_response):
        self.refresh_token = token_response["refresh_token"]
        self.refresh_token_expires_at = None
        if "refresh_token_expires_in" in token_response:
            self.refresh_token_expires_at = time.time() + token_response["refresh_token_expires_in"]
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(
                {
                    "refresh_token": self.refresh_token,
                    "refresh_token_expires_at": self.refresh_token_expires_at,
                }
            )
        )

    def do_token_refresh(self):
        if self.refresh_token is None:
            self.device_authorization_login()
            return
        if self.refresh_token_expires_at and self.refresh_token_expires_at < time.time() + 60:
            self.device_authorization_login()
            return
        data = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret
        r = requests.post(self.token_endpoint, data=data, timeout=30)
        if not r.ok:
            print(f"Failed to refresh token, with {r.text}")
            self.device_authorization_login()
            return
        token_response = r.json()
        if token_response.get("refresh_token", self.refresh_token) != self.refresh_token:
            self.update_refresh_token(token_response)
        self.update_access_token(token_response)

    def device_authorization_login(self):
        """Get an OIDC token by using Device Authorization Grant"""
        data = {"client_id": self.client_id}
        if self.scope:
            data["scope"] = self.scope
        if self.use_pkce:
            random_state = binascii.hexlify(os.urandom(8))
            code_verifier = binascii.hexlify(os.urandom(48))
            code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier).digest()).decode().replace("=", "")
            data["state"] = random_state
            data["code_challenge_method"] = "S256"
            data["code_challenge"] = code_challenge
        r = requests.post(self.device_flow_endpoint, data=data, timeout=30)
        if not r.ok:
            raise NotImplementedError(r.text)

        auth_response = r.json()

        print(f"{self.sso_name}\n")
        print("Open the following link directly and follow the instructions:")
        if "verification_uri_complete" in auth_response:
            print(f"    {auth_response['verification_uri_complete']}\n")
        else:
            print(f"    {auth_response['verification_url']}\n")
            print(f"    Code: {auth_response['user_code']}\n")
        print("Waiting for login...")

        while True:
            time.sleep(auth_response.get("interval", 5))
            data = {
                "client_id": self.client_id,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": auth_response["device_code"],
            }
            if self.client_secret:
                data["client_secret"] = self.client_secret
            if self.use_pkce:
                data["code_verifier"] = code_verifier
            r = requests.post(self.token_endpoint, data=data, timeout=30)
            if r.ok:
                token_response = r.json()
                self.update_access_token(token_response)
                self.update_refresh_token(token_response)
                break


class CernSSOCredentials(DeviceFlowCredentials):
    sso_name = "CERN Single Sign-On"
    use_pkce = True

    def __init__(self, client_id):
        super().__init__(
            client_id,
            token_endpoint="https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/token",
            device_flow_endpoint="https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/auth/device",
        )


class OperationsLogbook:
    url = "https://lblogbook.cern.ch/Operations/"

    def __init__(self):
        self.credentials = CernSSOCredentials("lhcb-logbook-run3")
        self._username = None
        self._password = None
        self._cookies = None
        if self.cache_path.exists():
            cache = json.loads(self.cache_path.read_text())
            self._cookies = cache["cookies"]
            self._expires = cache["expires"]
        if not self.check_credentials():
            self.login()

    def __str__(self):
        return f"OperationsLogbook({self.url}, username={self._username})"

    @property
    def cache_path(self):
        return CACHE_DIR / "operations-logbook-session.txt"

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.credentials.access_token}"}

    @property
    def cookies(self):
        if self._cookies is None or self._expires < time.time() + 60:
            self.login()
        return self._cookies

    @cookies.setter
    def cookies(self, cookies):
        self._cookies = cookies.get_dict()
        self._expires = min(c.expires for c in cookies)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(
                {
                    "cookies": self._cookies,
                    "expires": self._expires,
                }
            )
        )

    def login(self):
        while True:
            if self._username is None:
                self._username = prompt_toolkit.prompt("Enter Logbook Username: ")
            if self._password is None:
                self._password = prompt_toolkit.prompt("Enter Logbook Password: ", is_password=True)
            data = {
                "redir": "",
                "uname": self._username,
                "upassword": self._password,
                "remember": "1",
            }
            r = requests.post(
                self.url, files={k: (None, v) for k, v in data.items()}, headers=self.headers, allow_redirects=False
            )
            if r.status_code == 302:
                self.cookies = r.cookies
                if self.check_credentials():
                    break
            print("Login failed, please try again.")
            self._username = None
            self._password = None

    def check_credentials(self):
        try:
            user = re.search(r'Logged in as "([^"]+)"', self._get(self.url).text).group(1)
        except Exception as e:
            print(f"Failed to check credentials: {e}")
            return False
        else:
            self._username = user
            return True

    @staticmethod
    def _extract_form_data(r):
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find("form")
        if not form:
            raise NotImplementedError()
        default_form_data = {}
        # Find all input fields in the form
        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            value = input_tag.get("value", "")
            if name:
                default_form_data[name] = value

        form_data = {
            "unm": (None, default_form_data["unm"]),
            "upwd": (None, default_form_data["upwd"]),
            "jcmd": (None, default_form_data["jcmd"]),
            "smcmd": (None, default_form_data["smcmd"]),
            "inlineatt": (None, default_form_data["inlineatt"]),
            "new_entry": (None, default_form_data["new_entry"]),
            "entry_modified": (None, default_form_data["entry_modified"]),
            "entry_date": (None, default_form_data["entry_date"]),
            "Author": (None, default_form_data["Author"]),
            "Production_number": (None, default_form_data["Production_number"]),
            "GGUS_Ticket": (None, default_form_data["GGUS_Ticket"]),
            "Trello_JIRA_ticket": (None, default_form_data["Trello_JIRA_ticket"]),
            "CC": (None, default_form_data["CC"]),
            "Subject": (None, default_form_data["Subject"]),
            "Modified": (None, default_form_data["Modified"]),
            "Prefix": (None, default_form_data["Prefix"]),
            "Text": (None, default_form_data.get("Text", "")),
            "encoding": (None, default_form_data["encoding"]),
            "next_attachment": (None, default_form_data["next_attachment"]),
        }
        for i in range(1, int(default_form_data["next_attachment"])):
            form_data[f"attachment{i-1}"] = (None, default_form_data[f"attachment{i-1}"])
        form_data["attfile"] = (None, default_form_data["attfile"])
        return form_data

    def _get(self, url, **kwargs):
        r = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=30, **kwargs)
        r.raise_for_status()
        return r

    def _post(self, url, **kwargs):
        r = requests.post(url, headers=self.headers, cookies=self.cookies, timeout=30, **kwargs)
        r.raise_for_status()
        return r

    def create_post(self, issue_url, transformation_ids, subject, body, attachments):
        print(f"Creating logbook entry for {issue_url}")
        print(f"Transformations: {transformation_ids}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print(f"Attachments: {list(attachments)}")
        form_data = self._extract_form_data(self._get(f"{self.url}?cmd=New"))

        for name, blob in attachments.items():
            form_data["attfile"] = (name, blob)
            form_data["cmd"] = (None, "Upload")
            form_data = self._extract_form_data(self._post(self.url, files=form_data))

        form_data["Subject"] = (None, subject)
        form_data["Production_number"] = (None, ",".join(map(str, transformation_ids)))
        form_data["Trello_JIRA_ticket"] = (None, issue_url)
        form_data["Text"] = (None, body)
        form_data["System_32"] = (None, "Sprucing")
        form_data["cmd"] = (None, "Submit")
        r = self._post(self.url, files=form_data, allow_redirects=False)
        print(f"Logbook entry created at {r.headers['Location']}")


class ProdRequestsGitlabRepo:
    def __init__(self, *, with_auth: bool):
        cred_path = CACHE_DIR / "gitlab.json"
        cred = {}
        if cred_path.exists():
            cred = json.loads(cred_path.read_text())
        if with_auth:
            while True:
                private_token = cred.get("private_token")
                self.api = gitlab.Gitlab(url="https://gitlab.cern.ch", private_token=private_token)
                try:
                    self.api.auth()
                except gitlab.exceptions.GitlabAuthenticationError:
                    print("Gitlab authentication failed, please provide a new token.")
                    cred = {
                        "private_token": prompt_toolkit.prompt(
                            "Go to https://gitlab.cern.ch/lhcb-dpa/prod-requests/-/settings/access_tokens"
                            " and create a new token with':\n    * role; Developer\n"
                            "    * scopes: api\nThen paste it here:\n",
                            is_password=True,
                        )
                    }
                    cred_path.write_text(json.dumps(cred))
                else:
                    break
        else:
            self.api = gitlab.Gitlab(url="https://gitlab.cern.ch")

        self.project = self.api.projects.get("lhcb-dpa/prod-requests")

    def __str__(self):
        return f"ProdRequestsGitlabRepo({self.project.attributes['web_url']})"

    def get_issue(self, issue: int | str):
        if isinstance(issue, str):
            if not issue.startswith(self.project.attributes["web_url"]):
                raise ValueError("Invalid issue URL")
            issue = int(issue.split("/")[-1].split("#")[0])
        return self.project.issues.get(issue)

    def poll(self, *, do_status_update=False):
        all_tids = set()
        results = defaultdict(list)

        with Progress(*PROGRESS_COLUMNS) as progress:
            task = progress.add_task("Polling issues...", total=len(ISSUE_STATE_RESPONSIBLE))
            for state in ISSUE_STATE_RESPONSIBLE:
                issues = self.project.issues.list(labels=f"state::{state}", state="opened")
                task2 = progress.add_task(f"Polling {state} issues...", total=len(issues))
                for issue in issues:
                    issue = RepoIssue(issue)
                    results[state].append(issue)
                    for request_meta in issue.metadata.get("validations", {}).values():
                        all_tids |= set(request_meta["transform_ids"])
                    all_tids |= set(issue.all_transform_ids)
                    progress.advance(task2)
                progress.remove_task(task2)
                progress.update(task, advance=1)
        # If replication or removal has not been submitted yet we might have a None in the set
        if None in all_tids:
            all_tids.remove(None)

        if do_status_update:
            now = datetime.now(timezone.utc)
            file_statuses = asyncio.run(get_file_statuses(all_tids))
            with Progress(*PROGRESS_COLUMNS) as progress:
                task = progress.add_task("Updating issue metadata...", total=sum(map(len, results.values())))
                for state, issues in results.items():
                    for issue in issues:
                        for request_meta in issue.metadata.get("requests", {}).values():
                            request_meta.setdefault("file_status", {})
                            request_meta["file_status"] |= {
                                k: file_statuses[k] for k in issue.all_transform_ids if k in file_statuses
                            }
                        issue.metadata["last_updated"] = now.isoformat()
                        issue.update_metadata()
                        progress.update(task, advance=1)

        return dict(results)


async def _get_file_status(tid):
    loop = asyncio.get_running_loop()
    return returnValueOrRaise(
        await loop.run_in_executor(
            None,
            TransformationClient().getCounters,
            "TransformationFiles",
            ["TransformationID", "Status"],
            {"TransformationID": tid},
        )
    )


async def get_file_statuses(tids):
    tids = {int(tid) for tid in tids}
    file_statuses = defaultdict(dict)
    with Progress(*PROGRESS_COLUMNS) as progress:
        task1 = progress.add_task("Getting file counts...", total=len(tids))
        for result in asyncio.as_completed(map(_get_file_status, tids)):
            for meta, count in await result:
                file_statuses[int(meta["TransformationID"])][meta["Status"]] = count
            progress.update(task1, advance=1)
    return file_statuses


ISSUE_STATE_RESPONSIBLE = {
    "staging": "Computing",
    "preparing": "DPA",
    "run-validation": "Computing",
    "check-validation": "DPA",
    "ready": "Computing",
    "running-concurrent": "DPA",
    "update-end-run": "Computing",
    "running": "Computing",
    "debugging": "DPA",
    "checking": "DPA",
    "done": None,
}
