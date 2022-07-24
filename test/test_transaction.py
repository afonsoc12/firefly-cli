from datetime import datetime
from pathlib import Path

import pytest

from firefly_cli.parser import Parser
from firefly_cli.transaction import Transaction
from firefly_cli._version import get_versions

VERSION = get_versions()['version']

test_data = Path(__file__).parent.joinpath("test_data")


class TestTransaction:
    parser = Parser.add()

    @pytest.mark.parametrize(
        "fields, fields_missing",
        [
            ({"transaction": ["3,mocha,bank1,expense1"]}, []),
            ({"transaction": ["3,  mocha , bank1  , expense1  "]}, []),
            ({"transaction": [", mocha,, expense1"]}, ["amount", "source_name"]),
            ({"transaction": ["3,mocha, bank1"]}, ["destination_name"]),
            ({"transaction": ["3,mocha, bank1,"]}, ["destination_name"]),
            (
                {"transaction": ["mocha,, expense1"]},
                ["description", "destination_name"],
            ),
        ],
    )
    def test_mandatory_fields_missing(self, fields, fields_missing):
        """Asserts if the missing fields are the ones expected."""

        transaction = Transaction(**fields)
        transaction.parse_inline_transaction_to_attributes()

        assert transaction.mandatory_fields_missing() == fields_missing

    @pytest.mark.parametrize(
        "fields, arg_str",
        [
            (
                {
                    "transaction": [" 3 ,  mocha  , bank1 , expense1 "],
                    "date": datetime.strptime("1970-01-01", "%Y-%m-%d").astimezone(),
                    "type": "withdrawal",
                    "notes": f"Inserted by firefly-cli (v{VERSION})"
                },
                " 3 ,  mocha  , bank1 , expense1  --date 1970-01-01",
            )
        ],
    )
    def test_constructor_from_argparse(self, fields, arg_str):
        """Asserts if Transaction is the same if constructed from argparse or dict."""

        transaction = Transaction(**fields)

        args = TestTransaction.parser.parse_args([a for a in arg_str.split(" ") if a])

        transaction_argparse = Transaction.from_argparse(args)

        transaction.parse_inline_transaction_to_attributes()
        transaction_argparse.parse_inline_transaction_to_attributes()

        assert transaction == transaction_argparse

    @pytest.mark.parametrize(
        "arg_str, fields_expected",
        [
            (
                "3, mocha, bank1, expense1  --date 1970-01-01 --source-name bank2",
                {
                    "transaction": [""],
                    "amount": "3",
                    "description": "mocha",
                    "source_name": "bank2",
                    "destination_name": "expense1",
                    "date": datetime.strptime("1970-01-01", "%Y-%m-%d").astimezone(),
                    "type": "withdrawal",
                    "notes": f"Inserted by firefly-cli (v{VERSION})"
                },
            ),
            (
                "3, mocha, bank1  --date 1970-01-01 --destination-name expense3  --source-name bank2",
                {
                    "transaction": [""],
                    "amount": "3",
                    "description": "mocha",
                    "source_name": "bank2",
                    "destination_name": "expense3",
                    "date": datetime.strptime("1970-01-01", "%Y-%m-%d").astimezone(),
                    "type": "withdrawal",
                    "notes": f"Inserted by firefly-cli (v{VERSION})"
                },
            ),
            (
                "3, mocha, bank1  --date 1970-01-01 --source-name bank2 --type deposit",
                {
                    "transaction": [""],
                    "amount": "3",
                    "description": "mocha",
                    "source_name": "bank2",
                    "date": datetime.strptime("1970-01-01", "%Y-%m-%d").astimezone(),
                    "type": "deposit",
                    "notes": f"Inserted by firefly-cli (v{VERSION})"
                },
            ),
        ],
    )
    def test_parse_inline_transaction_to_attributes(self, arg_str, fields_expected):

        args = TestTransaction.parser.parse_args([a for a in arg_str.split(" ") if a])

        transaction = Transaction.from_argparse(args)
        transaction.parse_inline_transaction_to_attributes()
        transaction.transaction = None

        transaction_expected = Transaction(**fields_expected)
        transaction_expected.parse_inline_transaction_to_attributes()
        transaction_expected.transaction = None

        assert transaction == transaction_expected
