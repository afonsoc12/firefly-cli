from datetime import datetime

from cmd2 import Cmd2ArgumentParser


def get_add_parser():
    l_date_to_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d").astimezone()
    l_datetime_to_datetime = lambda s: datetime.strptime(
        s, "%Y-%m-%dT%H:%M:%S"
    ).astimezone()

    add_parser = Cmd2ArgumentParser()

    # Positional arguments
    add_parser.add_argument("transaction", nargs="*", help="Transaction data.")

    # Optional arguments (json header)
    add_parser.add_argument(
        "--apply-rules", default=True, dest="header__apply_rules", action="store_true"
    )
    add_parser.add_argument(
        "--fire-webhooks",
        default=False,
        dest="header__fire_webhooks",
        action="store_true",
    )

    # Optional arguments (json body)
    # Group mutually exclusive (date or datetime) stored as date.
    # Allows to specify transaction date or transaction datetime
    # Both stored as date
    group_date = add_parser.add_mutually_exclusive_group()
    group_date.add_argument(
        "--date",
        help="Transaction date (defaults to current date).",
        metavar="yyyy-mm-dd",
        default=datetime.now().astimezone(),
        type=l_date_to_datetime,
    )
    group_date.add_argument(
        "--datetime",
        metavar="yyyy-mm-ssTHH:MM:SS",
        dest="date",
        type=l_datetime_to_datetime,
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
