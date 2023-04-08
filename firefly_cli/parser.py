from argparse import ArgumentParser
from datetime import datetime

from cmd2 import Cmd2ArgumentParser

from firefly_cli._version import get_versions
from firefly_cli.api import FireflyAPI
from firefly_cli.configs import load_configs
from firefly_cli.utils import date_to_datetime, datetime_to_datetime

VERSION = get_versions()["version"]
configs = load_configs()
api = FireflyAPI(
    configs["firefly-cli"].get("url"), configs["firefly-cli"].get("api_token")
)


class Autocomplete:
    @staticmethod
    def accounts_name_provider(cmd, limit=20):
        return api.get_autocomplete_accounts(limit=limit)

    @staticmethod
    def description_provider(cmd, limit=10):
        pass
        # todo implement
        # return api.get_autocomplete_descriptions(limit=limit)


class Parser:
    @staticmethod
    def entrypoint(prog=None):
        parser = ArgumentParser(
            description="A command line interface for conveniently entering expenses in Firefly III.\nRun without arguments to start interactive mode.",
            usage="firefly-cli [-h] [-v]",
            add_help=False,
            prog=None,
        )

        # Optional arguments (json header)
        parser.add_argument(
            "-v", "--version", action="store_true", help="show version information"
        )
        parser.add_argument("-h", action="help", help="shows generic help message")
        parser.add_argument(
            "--help",
            action="store_true",
            help='shows firefly-cli help menu. Same as "firefly-cli help"',
        )

        return parser

    @staticmethod
    def accounts(prog=None):
        parser = Cmd2ArgumentParser(description="Shows account information.", prog=prog)

        # Optional arguments (json header)
        parser.add_argument("--json", action="store_true")

        parser.add_argument("--limit", help="The maximum number of accounts to display")

        parser.add_argument(
            "--type",
            default="all",
            choices=(
                "all",
                "asset",
                "cash",
                "expense",
                "revenue",
                "special",
                "hidden",
                "liability",
                "liabilities",
            ),
        )

        return parser

    @staticmethod
    def add(prog=None):

        parser = Cmd2ArgumentParser(
            description="Adds a new transaction to FireflyIII.",
            usage="add [comma-separated arguments] [-h] [--optional-arguments]",
            prog=None,
        )

        # Positional arguments
        parser.add_argument(
            "transaction",
            nargs="*",
            help="Transaction data in comma-separated format: Amount, Description , Source account, Destination account, Category, Budget",
        )

        # Optional arguments (json header)
        parser.add_argument(
            "-y",
            dest="bypass_prompt",
            action="store_true",
            help="Bypass confirmation prompt.",
        )
        parser.add_argument(
            "--apply-rules",
            default=True,
            dest="header__apply_rules",
            action="store_true",
        )
        parser.add_argument(
            "--fire-webhooks",
            default=False,
            dest="header__fire_webhooks",
            action="store_true",
        )

        # Optional arguments (json body)
        # Group mutually exclusive (date or datetime) stored as date.
        # Allows to specify transaction date or transaction datetime
        # Both stored as date
        group_date = parser.add_mutually_exclusive_group()
        group_date.add_argument(
            "--date",
            help="Transaction date (defaults to current date).",
            metavar="yyyy-mm-dd",
            default=datetime.now().astimezone(),
            type=date_to_datetime,
        )
        group_date.add_argument(
            "--datetime",
            metavar="yyyy-mm-ddTHH:MM:SS",
            dest="date",
            type=datetime_to_datetime,
        )

        parser.add_argument(
            "--type",
            default="withdrawal",
            choices=(
                "withdrawal",
                "deposit",
                "transfer",
            ),
        )
        parser.add_argument("--amount", type=float)
        parser.add_argument(
            "--description", choices_provider=Autocomplete.description_provider
        )
        parser.add_argument("--currency-id")
        parser.add_argument("--currency-code")
        parser.add_argument("--foreign-amount")
        parser.add_argument("--foreign-currency-id")
        parser.add_argument("--foreign-currency-code")
        parser.add_argument("--budget-id")
        parser.add_argument("--category-id")
        parser.add_argument("--category-name")
        parser.add_argument("--source-id")
        parser.add_argument(
            "--source-name", choices_provider=Autocomplete.accounts_name_provider
        )
        parser.add_argument("--destination-id")
        parser.add_argument(
            "--destination-name", choices_provider=Autocomplete.accounts_name_provider
        )
        parser.add_argument("--piggy-bank-id")
        parser.add_argument("--piggy-bank-name")
        parser.add_argument("--bill-id")
        parser.add_argument("--bill-name")
        parser.add_argument("--tags")
        parser.add_argument("--notes", default=f"Inserted by firefly-cli (v{VERSION})")
        parser.add_argument("--internal-reference")
        parser.add_argument("--external-id")
        parser.add_argument("--external-url")
        parser.add_argument("--interest-date")
        parser.add_argument("--book-date", metavar="YYYY-MM-DD", type=date_to_datetime)
        parser.add_argument(
            "--process-date", metavar="YYYY-MM-DD", type=date_to_datetime
        )
        parser.add_argument("--due-date", metavar="YYYY-MM-DD", type=date_to_datetime)
        parser.add_argument(
            "--payment-date", metavar="YYYY-MM-DD", type=date_to_datetime
        )
        parser.add_argument(
            "--invoice-date", metavar="YYYY-MM-DD", type=date_to_datetime
        )

        return parser

    @staticmethod
    def safe_string(args):
        args_str = " ".join(list(map(lambda x: f"'{x}'" if " " in x else x, args)))
        return args_str
