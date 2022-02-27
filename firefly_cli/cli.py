import json
from datetime import date

import cmd2
from tabulate import tabulate

from ._version import get_versions
from .api import FireflyAPI
from .configs import *
from .parsers import get_add_parser
from .transaction import Transaction
from .utils import prompt_continue


def help_exit():
    print("exit the application. Shorthand: x q Ctrl-D.")


class FireflyPrompt(cmd2.Cmd):
    prompt = "🐷 ➜ "
    cmd2.Cmd.set_window_title("🐷 firefly-cli")
    configs = load_configs()
    api = FireflyAPI(configs["API"].get("URL"), configs["API"].get("API_TOKEN"))

    is_url_set = True if configs["API"].get("URL") is not None else False
    is_api_token_set = True if configs["API"].get("API_TOKEN") is not None else False

    # Display information to update URL or API token, if not already set
    opt_text = ""
    if not (is_url_set and is_api_token_set):
        if is_url_set and not is_api_token_set:
            opt_text += '\n[WARNING] It appears that you have not set your API token yet.\nType "edit API_TOKEN <TOKEN>" to do so.\n'
        elif not is_url_set and is_api_token_set:
            opt_text += '\n[WARNING] It appears that you have not set your URL yet.\nType "edit URL <URL>" to do so.\n'
        elif not (is_url_set and is_api_token_set):
            opt_text += '\n[WARNING] It appears that you have not set neither your URL nor API token yet.\nType "edit URL <URL>" or "edit API_TOKEN <TOKEN>" to do so.\n'

    intro = f"""
Copyright {date.today().year} Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
Type \"license\" for more information.

Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

===== Status =====
  - URL: {configs["API"]["URL"] if is_url_set else "(not set)"}
  - API Token: {"*****" + configs["API"]["API_TOKEN"][-5:] if is_api_token_set else "(not set)"}
  - Connection: {"OK!" if api.api_test else "No connection!"}
  - Version: {get_versions()["version"]}
==================
{opt_text}
Type \"help\" to list commands.
"""

    @classmethod
    def refresh_api(cls):
        cls.configs = load_configs()
        cls.api = FireflyAPI(cls.configs["API"]["URL"], cls.configs["API"]["API_TOKEN"])
        print(
            "API refreshed. Current Status: {}".format(
                "OK!" if cls.api.api_test else "No connection!"
            )
        )

    def do_exit(self, _):
        print("Bye! Come store new transactions soon!")
        return True

    def do_license(self, _):
        print(
            f"""
Copyright {date.today().year} Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
        )

    def do_version(self, _):
        print(f"firefly-cli: v{get_versions()['version']}")

    def help_version(self):
        print("Displays version information.")

    def help_license(self):
        print("Displays License information.")

    def do_refresh(self, _):
        FireflyPrompt.refresh_api()

    def help_refresh(self):
        print("Refreshes API connection.")

    def do_edit(self, args):
        input_split = args.split(" ")
        if len(input_split) != 2:
            print(f'The command "edit" takes exactly two arguments. Provided: {args}')
        else:
            if input_split[0] == "URL" or input_split[0] == "API_TOKEN":
                self.configs["API"][input_split[0]] = input_split[1]
                save_configs_to_file(self.configs)
                FireflyPrompt.refresh_api()
            else:
                print(f'The argument "{input_split[0]}" is not recognised.')

    def help_edit(self):
        print(
            "Edits connection credentials:\n\t> edit URL http://<FireflyIII URL>:<Port>\n\t> edit API <API key>"
        )

    def do_accounts(self, args):
        # TODO: Implement with pagination based
        accounts = self.api.get_accounts()
        print(json.dumps(accounts, sort_keys=True, indent=4))

    def help_accounts(self):
        print("Shows your accounts.")

    def do_budgets(self, args):
        # TODO: Implement with pagination based
        budgets = self.api.get_budgets()
        print(json.dumps(budgets, sort_keys=True, indent=4))

    def help_budgets(self):
        print("Shows your budgets.")

    @cmd2.with_argparser(get_add_parser())
    def do_add(self, parser):
        trans = Transaction.from_input(parser)
        trans.parse_inline_transaction_to_attributes()

        missing_fields = trans.mandatory_fields_missing()
        if missing_fields:
            raise ValueError(
                f"Your transaction does not have these mandatory fields: {', '.join(missing_fields)}"
            )

        tab_header, tab_body = trans.get_tabulates()
        print(f"Transaction header:\n{tab_header}\n")
        print(f"Transaction Body:\n{tab_body}\n")

        if prompt_continue(extra_line=False, extra_msg=" adding the transaction"):
            try:
                response = self.api.create_transaction(trans)

                if response.status_code == 200:
                    print(f"Transaction successfully added!")
                elif response.status_code == 422:
                    print(f"The data provided is not valid!")
                    msg = response.json()["message"]
                    errors = response.json()["errors"]
                    print(f"\nMessage: {msg}")
                    print("Errors:")
                    for e in errors:
                        e_line = "; ".join(errors[e])
                        print(f"\t- {e}: {e_line}")

            except Exception:
                print(f"An error has occurred.")
                raise

    def default(self, args):
        if args.lower() in (
            "x",
            "q",
        ):
            return self.do_exit(args)

        print(
            '{} not recognized. Please type "help" to list the available commands'.format(
                args
            )
        )

    do_EOF = do_exit
    help_EOF = help_exit
