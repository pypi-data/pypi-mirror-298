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
import sys
from collections import defaultdict
from datetime import datetime, timezone

from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

from .actions import (
    ExtendEndRunAction,
    SubmitProductionsAction,
    UpdateIssueStateLabel,
    CheckValidationAction,
    CleanValidationAction,
    CompleteTransformationAction,
    CloseIssueAction,
)


def status_emoji(status):
    if status in {"Archived", "Completed"}:
        return ""
    if status in {"Cleaned", "Cleaning"}:
        return "🧹"
    if status in {"Active", "Idle"}:
        return "🏃"
    if status in {"Stopped"}:
        return "🫸"
    return "❔"


def analyse_active_productions(
    repo, *, states: set[str] = {"running", "running-concurrent", "update-end-run", "checking"}
):
    all_issues = repo.poll()
    actions = defaultdict(list)

    # Find validations that need to be submitted
    for issue in all_issues.get("run-validation", []):
        needs_submit = True
        for request_id, meta in issue.metadata.get("validations", {}).items():
            if meta["running"]:
                actions[issue].append(CheckValidationAction(issue, request_id))
                needs_submit = False
        if needs_submit:
            actions[issue].append(SubmitProductionsAction(issue))

    # Find productions that need to be submitted
    for issue in all_issues.get("ready", []):
        for request_id, meta in issue.metadata.get("validations", {}).items():
            if not meta["cleaned"]:
                actions[issue].append(CleanValidationAction(issue, request_id))
        actions[issue].append(SubmitProductionsAction(issue))

    issues_by_state = {k: v for k, v in all_issues.items() if k in states}
    # Find metadata for all relevant transformations
    all_tids = set()
    for state, issues in issues_by_state.items():
        for issue in issues:
            for request_id, request_meta in issue.metadata.get("requests", {}).items():
                all_tids |= set(request_meta["transform_ids"])
                all_tids.add(request_meta["removal"])
                all_tids.add(request_meta["replication"])
    retVal = TransformationClient().getTransformations(
        {"TransformationID": list(all_tids)},
        columns=["TransformationFamily", "TransformationID", "Type", "TransformationGroup", "CreationDate", "Status"],
    )
    tinfo = {x["TransformationID"]: x for x in returnValueOrRaise(retVal)}
    input_queries = returnValueOrRaise(TransformationClient().getBookkeepingQueries(list(tinfo)))

    # Create the table data
    last_update = datetime.fromtimestamp(0, timezone.utc)
    tables_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for state, issues in issues_by_state.items():
        for issue in issues:
            if issue.metadata.get("last_updated"):
                last_update = max(last_update, datetime.fromisoformat(issue.metadata["last_updated"]))
            for request_id, request_meta in issue.metadata.get("requests", {}).items():
                main_tid, merge_tid = request_meta["transform_ids"]
                if tinfo[merge_tid]["Type"] != "Merge":
                    raise NotImplementedError(tinfo[merge_tid])
                input_query = input_queries[main_tid]
                proc_pass = tinfo[main_tid]["TransformationGroup"].split("/")[-1]
                row_data = [f"[link={issue.url}]#{issue.issue.iid}[/link]"]
                row_data += [request_id, state, input_query["DataTakingConditions"]]
                row_data += [
                    f"{tid} {status_emoji(tinfo[tid]['Status'])}" if tid else "⚠️"
                    for tid in [main_tid, merge_tid, request_meta["removal"], request_meta["replication"]]
                ]
                row_data += [f"{input_query['StartRun']}:{input_query['EndRun']}"]
                file_status = request_meta.get("file_status", {}).get(str(main_tid), {})
                total = sum(file_status.values())
                row_data.append(total)
                row_data.append(file_status.get("Processed", 0))
                for status in ["MaxReset", "Problematic"]:
                    count = file_status.get(status, 0)
                    row_data.append(f"{count} 🚨" if count else 0)
                row_data.append(f"{file_status.get('Processed', 0) / total:.2%}" if total else "")
                n_checks = 0
                n_checks_passed = 0
                for check_name in ["DM Check", "PM Check", "DM Clean"]:
                    check_status = [
                        request_meta.setdefault("checks", {}).setdefault(check_name, {}).get(str(x))
                        for x in request_meta["transform_ids"]
                    ]
                    CHECK_DISPLAY = {None: "❔", True: "✅"}
                    row_data.append(" ".join(CHECK_DISPLAY[x] for x in check_status))
                    n_checks += len(check_status)
                    n_checks_passed += sum(filter(None, check_status))
                tables_data[input_query["ConfigVersion"]][proc_pass][input_query["EventType"]][
                    tinfo[main_tid]["Type"]
                ].append(row_data)

                if state == "checking" and n_checks == n_checks_passed:
                    actions[issue].append(CompleteTransformationAction(issue, main_tid))
                    actions[issue].append(CompleteTransformationAction(issue, merge_tid))
                    actions[issue].append(CompleteTransformationAction(issue, request_meta["removal"]))
                    actions[issue].append(UpdateIssueStateLabel(issue, "checking", "done"))

                # Ensure the start run is sensible
                if input_queries.get(main_tid, {}).get("StartRun") != issue.run_yaml.get("start_run"):
                    raise NotImplementedError(f"Start run mismatch: {issue} {main_tid}")
                if (
                    request_meta["removal"]
                    and input_queries.get(request_meta["removal"], {}).get("StartRun")
                    != input_queries[main_tid]["StartRun"]
                ):
                    raise NotImplementedError(f"Removal start run mismatch: {issue} {request_meta['removal']}")

                # Check if the end run needs to be extended
                main_value = input_queries.get(main_tid, {}).get("EndRun")
                expected_value = issue.run_yaml.get("end_run")
                if main_value != expected_value:
                    if state != "update-end-run":
                        raise NotImplementedError(
                            f"End run mismatch: {issue} {main_tid} {main_value} != {expected_value}"
                        )
                    actions[issue].append(ExtendEndRunAction(issue, main_tid, expected_value))
                    if request_meta["removal"] is not None:
                        actions[issue].append(ExtendEndRunAction(issue, request_meta["removal"], expected_value))
                    new_state = "running-concurrent" if issue.run_yaml["concurrent"] else "running"
                    actions[issue].append(UpdateIssueStateLabel(issue, "update-end-run", new_state))
                elif state == "update-end-run":
                    raise NotImplementedError(f"State is update-end-run there is nothing to change: {issue}")

                # Ensure the removal is consistent with the main transformation
                if request_meta["removal"] is not None:
                    removal_value = input_queries.get(request_meta["removal"], {}).get("EndRun")
                    if removal_value != main_value:
                        raise NotImplementedError(
                            f"Removal end run mismatch: {issue} {request_meta['removal']} {removal_value} != {main_value}"
                        )

    return last_update, tables_data, actions


def display_table(console, tables_data):
    # Create the rich tables from the table data
    tables = defaultdict(list)
    for config in sorted(tables_data):
        for proc_pass in sorted(tables_data[config]):
            section = f"# {config} {proc_pass}"
            for eventtype in sorted(tables_data[config][proc_pass]):
                for tran_type, table_rows in sorted(tables_data[config][proc_pass][eventtype].items()):
                    table = Table(
                        *["Issue", "Request", "State", "Conditions", tran_type, "Merging", "Removal", "Replication"],
                        *["Runs", "RAWs", "Processed", "MaxReset", "Problematic", "% Done"],
                        *["DM Check", "PM Check", "DM Clean"],
                        row_styles=["dim", ""],
                        title=f"[bold]{eventtype}",
                    )
                    for row in sorted(table_rows, key=lambda x: x[4]):
                        table.add_row(*map(str, row))
                    tables[section].append(table)

    # Make the columns the same width across all tables
    for cols in zip(*(x.columns for section_tables in tables.values() for x in section_tables)):
        width = max(console.measure(cell).maximum for col in cols for cell in col.cells)
        width = max(width, len(cols[0].header))
        for col in cols:
            col.width = width
    # Display the tables
    for section, tables in tables.items():
        console.print(Markdown(section))
        for table in tables:
            console.print(table)


def display_actions(console, actions, *, execute=False):
    console.print(Markdown("# Recommended Actions"))
    for issue, action_list in actions.items():
        lines = [f"## {issue.url} ({issue.state})\n"]
        lines.extend(f"- {action.message()}" for action in action_list)
        console.print(Markdown("\n".join(lines)))
        if not execute:
            continue

        match response := Prompt.ask("Do you want to run these actions?", choices=["yes", "no", "quit"], default="no"):
            case "yes":
                for action in action_list:
                    action.run()
            case "quit":
                sys.exit(0)
            case "no":
                continue
            case _:
                raise NotImplementedError(f"Invalid response: {response}")
