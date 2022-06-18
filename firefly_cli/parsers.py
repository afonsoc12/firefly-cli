from argparse import ArgumentParser
from datetime import datetime

from cmd2 import Cmd2ArgumentParser

from firefly_cli.api import FireflyAPI
from firefly_cli.configs import load_configs
from firefly_cli.utils import date_to_datetime, datetime_to_datetime

configs = load_configs()
api = FireflyAPI(
    configs["firefly-cli"].get("url"), configs["firefly-cli"].get("api_token")
)


def source_name_provider(prompt):
    return api.get_autocomplete_accounts()


def get_entrypoint():
    parser = ArgumentParser(
        description="Shows account information a new transaction to FireflyIII.",
        # usage="accounts [comma-separated arguments] [-h] [--optional-arguments]",
    )

    # Positional arguments
    parser.add_argument("transaction", nargs="*", help="Transaction data.")

    # Optional arguments (json header)
    parser.add_argument(
        "--json", default=True, dest="header__apply_rules", action="store_true"
    )

def get_show_accounts():
    parser = Cmd2ArgumentParser(
        description="Shows account information a new transaction to FireflyIII.",
        # usage="accounts [comma-separated arguments] [-h] [--optional-arguments]",
    )

    # Positional arguments
    parser.add_argument("transaction", nargs="*", help="Transaction data.")

    # Optional arguments (json header)
    parser.add_argument(
        "--json", action="store_true"
    )

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


def get_add_parser():

    parser = Cmd2ArgumentParser(
        description="Adds a new transaction to FireflyIII.",
        usage="add [comma-separated arguments] [-h] [--optional-arguments]",
    )

    # Positional arguments
    parser.add_argument("transaction", nargs="*", help="Transaction data.")

    # Optional arguments (json header)
    parser.add_argument(
        "--apply-rules", default=True, dest="header__apply_rules", action="store_true"
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
    parser.add_argument("--description")
    parser.add_argument("--currency-id")
    parser.add_argument("--currency-code")
    parser.add_argument("--foreign-amount")
    parser.add_argument("--foreign-currency-id")
    parser.add_argument("--foreign-currency-code")
    parser.add_argument("--budget-id")
    parser.add_argument("--category-id")
    parser.add_argument("--category-name")
    parser.add_argument("--source-id")
    parser.add_argument("--source-name", choices_provider=source_name_provider)
    parser.add_argument("--destination-id")
    parser.add_argument("--destination-name")
    parser.add_argument("--piggy-bank-id")
    parser.add_argument("--piggy-bank-name")
    parser.add_argument("--bill-id")
    parser.add_argument("--bill-name")
    parser.add_argument("--tags")
    parser.add_argument("--notes")
    parser.add_argument("--internal-reference")
    parser.add_argument("--external-id")
    parser.add_argument("--external-url")
    parser.add_argument("--interest-date")
    parser.add_argument("--book-date", metavar="YYYY-MM-DD", type=date_to_datetime)
    parser.add_argument("--process-date", metavar="YYYY-MM-DD", type=date_to_datetime)
    parser.add_argument("--due-date", metavar="YYYY-MM-DD", type=date_to_datetime)
    parser.add_argument("--payment-date", metavar="YYYY-MM-DD", type=date_to_datetime)
    parser.add_argument("--invoice-date", metavar="YYYY-MM-DD", type=date_to_datetime)

    return parser
