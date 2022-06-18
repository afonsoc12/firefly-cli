import json
from pathlib import Path

import pytest

from firefly_cli.api import FireflyAPI

test_data = Path(__file__).parent.joinpath("test_data") / "api"


class TestAPI:

    with open(test_data / "accounts.json", "r") as f:
        accounts_data = json.loads(f.read())

    with open(test_data / "accounts_full.json", "r") as f:
        accounts_full = json.loads(f.read())

    with open(test_data / "accounts_empty.json", "r") as f:
        accounts_empty = json.loads(f.read())

    with open(test_data / "accounts_pagination.json", "r") as f:
        accounts_pagination = json.loads(f.read())

    @pytest.mark.parametrize(
        "data, account_names",
        [
            (
                accounts_full,
                accounts_data["test_process_accounts_autocomplete"]["expected"][0],
            ),
            (
                accounts_empty,
                accounts_data["test_process_accounts_autocomplete"]["expected"][1],
            ),
            (
                accounts_pagination,
                accounts_data["test_process_accounts_autocomplete"]["expected"][2],
            ),
        ],
    )
    def test_process_accounts_autocomplete(self, data, account_names):
        """Asserts if the missing fields are the ones expected."""

        assert FireflyAPI.process_accounts(data, format="autocomplete") == account_names

    @pytest.mark.parametrize(
        "data, accounts_proc",
        [
            (
                accounts_full,
                accounts_data["test_process_accounts_full"]["all"]["expected"],
            ),
            (
                accounts_empty,
                accounts_data["test_process_accounts_full"]["empty"]["expected"],
            ),
            (
                accounts_pagination,
                accounts_data["test_process_accounts_full"]["pagination"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["asset"]["data"],
                accounts_data["test_process_accounts_full"]["asset"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["cash"]["data"],
                accounts_data["test_process_accounts_full"]["cash"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["expense"]["data"],
                accounts_data["test_process_accounts_full"]["expense"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["revenue"]["data"],
                accounts_data["test_process_accounts_full"]["revenue"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["special"]["data"],
                accounts_data["test_process_accounts_full"]["special"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["hidden"]["data"],
                accounts_data["test_process_accounts_full"]["hidden"]["expected"],
            ),
            (
                accounts_data["test_process_accounts_full"]["liability"]["data"],
                accounts_data["test_process_accounts_full"]["liability"]["expected"],
            ),
        ],
    )
    def test_process_accounts_full(self, data, accounts_proc):
        """Asserts if the missing fields are the ones expected."""
        import json

        assert FireflyAPI.process_accounts(data, format="full") == accounts_proc
