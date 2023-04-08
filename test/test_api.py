from test.utils import load_test_data

import pytest

from firefly_cli import FireflyAPI, Transaction
from firefly_cli.configs import load_configs
from firefly_cli.parser import Parser


class TestAPI:
    test_data = load_test_data(__name__, "test_data.json")
    accounts_full = load_test_data(__name__, "api_accounts_full.json")
    accounts_empty = load_test_data(__name__, "api_accounts_empty.json")
    accounts_pagination = load_test_data(__name__, "api_accounts_pagination.json")
    transactions_response = load_test_data(__name__, "api_transactions_response.json")
    about_user = load_test_data(__name__, "api_about_user.json")

    def test_test_api_connection(self, api):
        endpoint = "about/user"
        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.about_user,
            status_code=200,
        )

        assert api.get_about_user()

    def test_get_about_user(self, api):
        endpoint = "about/user"
        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.about_user,
            status_code=200,
        )

        assert api.get_about_user()["data"]["attributes"]["email"] == "test@test.com"

    def test_get_accounts(self, api):
        endpoint = "accounts"
        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}?type=all",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )

        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}?type=all&page=1",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[0],
            status_code=200,
        )

        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}?type=all&page=2",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[1],
            status_code=200,
        )

        assert (
            FireflyAPI.count_total_page_elements(
                api.get_accounts(account_type="all", limit=3)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                api.get_accounts(account_type="all", limit=3, pagination=True)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                api.get_accounts(account_type="all", limit=52)
            )
            == 43
        )
        assert (
            FireflyAPI.count_total_page_elements(
                api.get_accounts(account_type="all", limit=52, pagination=True)
            )
            == 86
        )

    def test_get_budgets(self):
        # todo test get_budgets
        pass

    def test_get_autocomplete_accounts(self, api):
        endpoint = "accounts"
        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )

        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}?page=1",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[0],
            status_code=200,
        )

        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}?page=2",
            headers={"Content-Type": "application/json"},
            json=self.accounts_pagination[1],
            status_code=200,
        )

        assert (
            api.get_autocomplete_accounts()
            == self.test_data["test_process_accounts_autocomplete"]["expected"][2][:20]
        )
        assert (
            api.get_autocomplete_accounts(limit=10)
            == self.test_data["test_process_accounts_autocomplete"]["expected"][2][:10]
        )
        assert (
            api.get_autocomplete_accounts(limit=20)
            == self.test_data["test_process_accounts_autocomplete"]["expected"][2][:20]
        )
        assert (
            api.get_autocomplete_accounts(limit=52)
            == self.test_data["test_process_accounts_autocomplete"]["expected"][2][:52]
        )
        assert (
            api.get_autocomplete_accounts(limit=100)
            == self.test_data["test_process_accounts_autocomplete"]["expected"][2][:100]
        )

    def test_create_transaction(self, api):
        endpoint = "transactions"

        arg_str = "3, mocha, bank1  --date 1970-01-01 --destination-name expense3 --source-name bank"
        parser = Parser.add().parse_args([a for a in arg_str.split(" ") if a])
        transaction = Transaction.from_argparse(parser)
        transaction.parse_inline_transaction_to_attributes()

        api.rc.get_adapter("https://").register_uri(
            "POST",
            f"{api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.transactions_response,
            status_code=200,
        )

        response = api.create_transaction(transaction)

        assert response.json() == self.transactions_response

    def test_payload_formatter(self, api):

        arg_str = "3, mocha, bank1  --date 1970-01-01 --destination-name expense3 --source-name bank2"
        parser = Parser.add().parse_args([a for a in arg_str.split(" ") if a])
        transaction = Transaction.from_argparse(parser)
        transaction.parse_inline_transaction_to_attributes()

        payload = api.payload_formatter(transaction)

        assert len([k for k in payload.keys() if k.startswith("header__")]) == 0
        assert len(payload.keys()) <= 5
        assert "transactions" in payload and isinstance(payload["transactions"], list)
        assert {
            "type",
            "amount",
            "description",
            "source_name",
            "destination_name",
        }.issubset(payload["transactions"][0].keys())

    def test_refresh_api(self, api):
        assert isinstance(api.refresh_api(load_configs()), FireflyAPI)

    @pytest.mark.parametrize(
        "data, account_names",
        [
            (
                accounts_full,
                test_data["test_process_accounts_autocomplete"]["expected"][0],
            ),
            (
                accounts_empty,
                test_data["test_process_accounts_autocomplete"]["expected"][1],
            ),
            (
                accounts_pagination,
                test_data["test_process_accounts_autocomplete"]["expected"][2],
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
                test_data["test_process_accounts_full"]["all"]["expected"],
            ),
            (
                accounts_empty,
                test_data["test_process_accounts_full"]["empty"]["expected"],
            ),
            (
                accounts_pagination,
                test_data["test_process_accounts_full"]["pagination"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["asset"]["data"],
                test_data["test_process_accounts_full"]["asset"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["cash"]["data"],
                test_data["test_process_accounts_full"]["cash"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["expense"]["data"],
                test_data["test_process_accounts_full"]["expense"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["revenue"]["data"],
                test_data["test_process_accounts_full"]["revenue"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["special"]["data"],
                test_data["test_process_accounts_full"]["special"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["hidden"]["data"],
                test_data["test_process_accounts_full"]["hidden"]["expected"],
            ),
            (
                test_data["test_process_accounts_full"]["liability"]["data"],
                test_data["test_process_accounts_full"]["liability"]["expected"],
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

    def test_flush_cache(self, api):
        endpoint = "about/user"
        api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.about_user,
            status_code=200,
        )

        # Perform a query to cache results
        req1 = api._get(endpoint=endpoint, cache=True, request_raw=True)
        assert not req1.from_cache

        # Second request should use cached results
        req2 = api._get(endpoint=endpoint, cache=True, request_raw=True)
        assert req2.from_cache and req1.cache_key == req2.cache_key

        # Refresh API
        api.rc.cache.clear()
        assert len(list(api.rc.cache.keys())) == 0

        # Third request should not see any cached results
        req3 = api._get(endpoint=endpoint, cache=True, request_raw=True)
        assert not req3.from_cache and req3.cache_key in (
            req1.cache_key,
            req2.cache_key,
        )
