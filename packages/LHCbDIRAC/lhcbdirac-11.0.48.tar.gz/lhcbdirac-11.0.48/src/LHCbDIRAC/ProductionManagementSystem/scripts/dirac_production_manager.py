#!/usr/bin/env python
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
import argparse

import DIRAC
from DIRAC.Core.Security.Properties import PRODUCTION_MANAGEMENT
from rich.console import Console
from rich.prompt import Prompt


def main():
    parser = argparse.ArgumentParser(description="Manage LHCbDIRAC production requests")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser = subparsers.add_parser("show-requests", help="Show the current status of the production requests")
    subparser.set_defaults(func=show_requests)
    subparser.add_argument("--execute-actions", action="store_true", help="Execute the actions")

    subparser = subparsers.add_parser("update-metadata", help="Update the metadata stored on GitLab")
    subparser.set_defaults(func=update_metadata)

    args = parser.parse_args()
    args.func(args)


def show_requests(args):
    DIRAC.initialize()
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools import ProdRequestsGitlabRepo
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools.monitoring import (
        analyse_active_productions,
        display_table,
        display_actions,
    )

    if args.execute_actions:
        DIRAC.initialize(security_expression=PRODUCTION_MANAGEMENT)
        match Prompt.ask("Update metadata?", choices=["yes", "no"], default="yes"):
            case "yes":
                update_metadata(args)

    repo = ProdRequestsGitlabRepo(with_auth=args.execute_actions)
    last_update, tables_data, actions = analyse_active_productions(repo)
    console = Console()
    console.rule()
    display_table(console, tables_data)
    console.print(f"Last update: {last_update}")
    console.rule()
    display_actions(console, actions, execute=args.execute_actions)


def update_metadata(args):
    DIRAC.initialize(security_expression=PRODUCTION_MANAGEMENT)
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools import ProdRequestsGitlabRepo

    repo = ProdRequestsGitlabRepo(with_auth=True)
    repo.poll(do_status_update=True)


if __name__ == "__main__":
    main()
