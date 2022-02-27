from datetime import datetime

from cmd2 import Cmd2ArgumentParser


def get_add_parser():
    l_date_to_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d").astimezone()

    add_parser = Cmd2ArgumentParser()

    # Positional arguments
    add_parser.add_argument("transaction", nargs="*", help="Transaction data.")

    # Optional arguments (json header)
    # todo make sure its converted to bool
    add_parser.add_argument(
        "--apply_rules", default=True, dest="header__apply_rules", type=bool
    )
    add_parser.add_argument(
        "--fire_webhooks", default=False, dest="header__fire_webhooks", type=bool
    )

    # Optional arguments (json body)
    add_parser.add_argument(
        "--date",
        help="Transaction date (defaults to current date).",
        metavar="YYYY-MM-DD",
        default=datetime.now().astimezone(),
        type=l_date_to_datetime,
    )
    add_parser.add_argument(
        "--type",
        default="withdrawal",
        choices=(
            "withdrawal",
            "deposit",
            "transfer",
        ),
    )
    add_parser.add_argument("--amount", type=float)
    add_parser.add_argument("--description")
    add_parser.add_argument("--currency_id")
    add_parser.add_argument("--currency_code")
    add_parser.add_argument("--foreign_amount")
    add_parser.add_argument("--foreign_currency_id")
    add_parser.add_argument("--foreign_currency_code")
    add_parser.add_argument("--budget_id")
    add_parser.add_argument("--category_id")
    add_parser.add_argument("--category_name")
    add_parser.add_argument("--source_id")
    add_parser.add_argument("--source_name")
    add_parser.add_argument("--destination_id")
    add_parser.add_argument("--destination_name")
    add_parser.add_argument("--piggy_bank_id")
    add_parser.add_argument("--piggy_bank_name")
    add_parser.add_argument("--bill_id")
    add_parser.add_argument("--bill_name")
    add_parser.add_argument("--tags")
    add_parser.add_argument("--notes")
    add_parser.add_argument("--internal_reference")
    add_parser.add_argument("--external_id")
    add_parser.add_argument("--external_url")
    add_parser.add_argument("--interest_date")
    add_parser.add_argument(
        "--book_date", metavar="YYYY-MM-DD", type=l_date_to_datetime
    )
    add_parser.add_argument(
        "--process_date", metavar="YYYY-MM-DD", type=l_date_to_datetime
    )
    add_parser.add_argument("--due_date", metavar="YYYY-MM-DD", type=l_date_to_datetime)
    add_parser.add_argument(
        "--payment_date", metavar="YYYY-MM-DD", type=l_date_to_datetime
    )
    add_parser.add_argument(
        "--invoice_date", metavar="YYYY-MM-DD", type=l_date_to_datetime
    )

    return add_parser
