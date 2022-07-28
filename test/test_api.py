import json
from pathlib import Path

import pytest
from requests_cache import CachedSession
from requests_mock import Adapter

from firefly_cli.api import FireflyAPI

test_data = Path(__file__).parent.joinpath("test_data") / "api"

URL = "https://test.com"


class TestAPI:

    with open(test_data / "accounts.json", "r") as f:
        accounts_data = json.loads(f.read())

    with open(test_data / "accounts_full.json", "r") as f:
        accounts_full = json.loads(f.read())

    with open(test_data / "accounts_empty.json", "r") as f:
        accounts_empty = json.loads(f.read())

    with open(test_data / "accounts_pagination.json", "r") as f:
        accounts_pagination = json.loads(f.read())

    @pytest.fixture(scope="function")
    def mock_api(self):
        """Fixture that provides a CachedSession that will make mock requests where it would normally
        make real requests"""

        api = FireflyAPI(hostname=URL, auth_token="test", check_connection=False)

        adapter = Adapter()

        session = CachedSession(backend="memory")
        session.mount("https://", adapter)

        api.rc = session

        yield api

    def test_get_accounts(self, mock_api):
        endpoint = "accounts"
        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}?type=all",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )

        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}?type=all&page=1",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[0],
            status_code=200,
        )

        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}?type=all&page=2",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[1],
            status_code=200,
        )

        assert (
            FireflyAPI.count_total_page_elements(
                mock_api.get_accounts(account_type="all", limit=3)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                mock_api.get_accounts(account_type="all", limit=3, pagination=True)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                mock_api.get_accounts(account_type="all", limit=52)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                mock_api.get_accounts(account_type="all", limit=52, pagination=True)
            )
            == 86
        )

    def test_get_autocomplete_accounts(self, mock_api):
        endpoint = "accounts"
        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )

        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}?page=1",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[0],
            status_code=200,
        )

        mock_api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{mock_api.api_url}{endpoint}?page=2",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[1],
            status_code=200,
        )

        assert (
            mock_api.get_autocomplete_accounts()
            == self.accounts_data["test_process_accounts_autocomplete"]["expected"][2][
                :20
            ]
        )
        assert (
            mock_api.get_autocomplete_accounts(limit=10)
            == self.accounts_data["test_process_accounts_autocomplete"]["expected"][2][
                :10
            ]
        )
        assert (
            mock_api.get_autocomplete_accounts(limit=20)
            == self.accounts_data["test_process_accounts_autocomplete"]["expected"][2][
                :20
            ]
        )
        assert (
            mock_api.get_autocomplete_accounts(limit=52)
            == self.accounts_data["test_process_accounts_autocomplete"]["expected"][2][
                :52
            ]
        )
        assert (
            mock_api.get_autocomplete_accounts(limit=100)
            == self.accounts_data["test_process_accounts_autocomplete"]["expected"][2][
                :100
            ]
        )

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
        assert (
            FireflyAPI.process_accounts(data, format="autocomplete", limit=10)
            == account_names[:10]
        )
        assert (
            FireflyAPI.process_accounts(data, format="autocomplete", limit=52)
            == account_names[:52]
        )
        assert (
            FireflyAPI.process_accounts(data, format="autocomplete", limit=100)
            == account_names[:100]
        )

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
        assert FireflyAPI.process_accounts(data, format="full") == accounts_proc
        assert FireflyAPI.process_accounts(data, format="full", limit=10) == {
            k: v[:10] for k, v in accounts_proc.items()
        }
        assert FireflyAPI.process_accounts(data, format="full", limit=52) == {
            k: v[:52] for k, v in accounts_proc.items()
        }
        assert FireflyAPI.process_accounts(data, format="full", limit=100) == {
            k: v[:100] for k, v in accounts_proc.items()
        }

    def test_count_total_page_elements(self):
        assert FireflyAPI.count_total_page_elements(self.accounts_empty) == 0
        assert FireflyAPI.count_total_page_elements(self.accounts_full) == 43
        assert FireflyAPI.count_total_page_elements(self.accounts_pagination) == 86
