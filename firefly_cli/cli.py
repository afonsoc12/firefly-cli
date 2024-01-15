import json
from datetime import date

import cmd2

from firefly_cli._version import get_versions
from firefly_cli.api import FireflyAPI
from firefly_cli.bcolors import bcolors
from firefly_cli.configs import *
from firefly_cli.parser import Parser
from firefly_cli.transaction import Transaction
from firefly_cli.utils import prompt_continue, tabulate


class FireflyPrompt(cmd2.Cmd):
    prompt = "🐷 ➜ "
    cmd2.Cmd.set_window_title("🐷 firefly-cli")
    configs = load_configs()
    api = FireflyAPI(
        configs["firefly-cli"].get("url"), configs["firefly-cli"].get("api_token")
    )

    is_url_set = True if configs["firefly-cli"].get("url") else False
    is_api_token_set = True if configs["firefly-cli"].get("api_token") else False

    # Display information to update URL or API token, if not already set
    opt_text = ""
    if not (is_url_set and is_api_token_set):
        if is_url_set and not is_api_token_set:
            opt_text += f'\n{bcolors.WARNING}[WARNING] It appears that you have not set your API token yet.{bcolors.ENDC}\nType "edit API_TOKEN <TOKEN>" to do so.\n'
        elif not is_url_set and is_api_token_set:
            opt_text += f'\n{bcolors.WARNING}[WARNING] It appears that you have not set your URL yet.{bcolors.ENDC}\nType "edit URL <URL>" to do so.\n'
        elif not (is_url_set and is_api_token_set):
            opt_text += f'\n{bcolors.WARNING}[WARNING] It appears that you have not set neither your URL nor API token yet.{bcolors.ENDC}\nType "edit URL <URL>" or "edit API_TOKEN <TOKEN>" to do so.\n'

    intro = f"""
Copyright {date.today().year} Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
Type \"license\" for more information.

Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

=============== Status ===============
  - URL: {configs["firefly-cli"]["url"] if is_url_set else "(not set)"}
  - API Token: {"*****" + configs["firefly-cli"]["api_token"][-5:] if is_api_token_set else "(not set)"}
  - Version: v{get_versions()["version"]}
  - Connection: {f"{bcolors.OKGREEN}OK!{bcolors.ENDC}" if api.api_test else f"{bcolors.FAIL}No connection!{bcolors.ENDC}"}
======================================
{opt_text}
Type \"help\" to list commands.
"""

    def __init__(self):
        super(FireflyPrompt, self).__init__(allow_cli_args=False)

    @staticmethod
    def format_version():
        return f"firefly-cli: {get_versions()['version']}"

    def do_license(self, _):
        self.poutput(
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

    def help_license(self):
        self.poutput("Displays License information.")

    def do_version(self, _):
        self.poutput(FireflyPrompt.format_version())

    def help_version(self):
        self.poutput("Displays version information.")

    def do_refresh(self, _):
        self.configs = load_configs()
        self.api = FireflyAPI.refresh_api(self.configs)
        self.poutput(
            f"API refreshed. Current Status: {f'{bcolors.OKGREEN}OK!{bcolors.ENDC}' if self.api.api_test else f'{bcolors.FAIL}No connection!{bcolors.ENDC}'}"
        )

    def help_refresh(self):
        self.poutput("Refreshes API connection.")

    @cmd2.with_argument_list()
    def do_edit(self, argslist):
        if len(argslist) != 2:
            self.poutput(
                f"The command 'edit' takes exactly two arguments. Provided: {' '.join(argslist)}"
            )
        else:
            if argslist[0].casefold() == "url" or argslist[0].casefold() == "api_token":
                self.configs["firefly-cli"][argslist[0]] = argslist[1]
                save_configs_to_file(self.configs)
                self.api = FireflyAPI.refresh_api(self.configs)
            else:
                self.poutput(f'The argument "{argslist[0]}" is not recognised.')

    def help_edit(self):
        self.poutput(
            "Edits connection credentials:\n\t> edit url https://<FireflyIII URL>:<Port>\n\t> edit api <API key>"
        )

    @cmd2.with_argparser(Parser.accounts())
    def do_accounts(self, parser):
        accounts = self.api.get_accounts(limit=parser.limit)
        if parser.json:
            self.poutput(json.dumps(accounts, sort_keys=True, indent=4))
        else:
            accounts_pretty = FireflyAPI.process_accounts(accounts, format="full")
            self.poutput(tabulate(accounts_pretty, header_fmt="capitalise_from_snake"))

    def help_accounts(self):
        self.poutput("Shows your accounts.")

    def do_budgets(self, args):
        # TODO: Implement with pagination based
        budgets = self.api.get_budgets()
        self.poutput(json.dumps(budgets, sort_keys=True, indent=4))

    def help_budgets(self):
        self.poutput("Shows your budgets.")

    @cmd2.with_argparser(Parser.add())
    def do_add(self, parser):
        trans = Transaction.from_argparse(parser)
        trans.parse_inline_transaction_to_attributes()

        missing_fields = trans.mandatory_fields_missing()
        if missing_fields:
            raise ValueError(
                f"Your transaction does not have these mandatory fields: {', '.join(missing_fields)}"
            )

        tab_header, tab_body = trans.get_tabulates()
        self.poutput(f"Transaction header:\n{tab_header}\n")
        self.poutput(f"Transaction body:\n{tab_body}\n")

        if parser.bypass_prompt or prompt_continue(
            extra_line=False, extra_msg=" adding the transaction"
        ):
            try:
                response = self.api.create_transaction(trans)

                if response.status_code == 200:
                    self.poutput(f"Transaction successfully added!")
                elif response.status_code == 422:
                    self.poutput(f"The data provided is not valid!")
                    msg = response.json()["message"]
                    errors = response.json()["errors"]
                    self.poutput(f"\nMessage: {msg}")
                    self.poutput("Errors:")
                    for e in errors:
                        e_line = "; ".join(errors[e])
                        self.poutput(f"\t- {e}: {e_line}")

            except Exception:
                self.poutput(f"An error has occurred.")
                raise

    def do_exit(self, _):
        self.poutput("Bye! Come store new transactions soon!")
        return True

    def help_exit(self):
        return self.poutput("Exits the application. Shorthand: q Ctrl-D.")

    def default(self):
        # todo default when arg not recognised
        pass

    do_q = do_exit
    help_q = help_exit

    do_EOF = do_exit
    help_EOF = help_exit
