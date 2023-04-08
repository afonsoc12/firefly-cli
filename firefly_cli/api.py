from contextlib import nullcontext

from requests_cache import CachedSession

from firefly_cli.transaction import Transaction

"""FireflyIII API Driver.

API documentation: https://api-docs.firefly-iii.org
"""


class FireflyAPI:
    """Firefly API driver Class."""

    rc = CachedSession(
        "firefly_cli_http_cache", backend="sqlite", use_temp=True, expire_after=43200
    )
    rc.cache.clear()

    def __init__(self, hostname, auth_token, check_connection=True):
        self.headers = {"Authorization": "Bearer " + auth_token if auth_token else ""}
        self.hostname = (
            hostname
            if hostname is None or not hostname.endswith("/")
            else hostname[:-1]
        )  # Remove trailing backslash
        self.api_url = self.hostname + "/api/v1/" if hostname else self.hostname
        self.api_test = self.test_api_connection() if check_connection else False

    def _post(self, endpoint, payload):
        """Handles general POST requests."""

        response = self.rc.post(
            "{}{}".format(self.api_url, endpoint),
            json=payload,
            # Pass extra headers, or it redirects to login
            headers={
                **self.headers,
                **{"Content-Type": "application/json", "accept": "application/json"},
            },
        )

        return response

    def _get(self, endpoint, params={}, cache=False, request_raw=False, timeout=2):
        """Handles general GET requests."""

        with self.rc.cache_disabled() if not cache else nullcontext():
            response = self.rc.get(
                "{}{}".format(self.api_url, endpoint),
                params=params,
                headers=self.headers,
                timeout=timeout,
            )

        return response.json() if not request_raw else response

    def test_api_connection(self):
        """Tests API connection."""
        try:
            _ = self.get_about_user()
            return True
        except:
            return False

    def get_about_user(self):
        """Returns user information."""

        return self._get("about/user")

    def get_accounts(
        self, account_type="asset", cache=False, pagination=False, limit=None
    ):
        """Returns all user accounts.

        If limit is set, it will be rounded up to the nearest 50. If limit is smaller than per_page, then a single
        page will be requested.
        """
        params = {
            "type": account_type if account_type else None,
            "page": 1 if pagination else None,
        }
        pages = []
        page = self._get("accounts", params=params, cache=cache)

        pages.append(page)

        if pagination:
            while (
                "next" in page["links"]
                and FireflyAPI.count_total_page_elements(pages) < limit
            ):
                params["page"] = page["meta"]["pagination"]["current_page"] + 1
                page = self._get("accounts", params=params, cache=cache)
                pages.append(page)

        return pages

    def get_budgets(self):
        """Returns budgets of the user."""

        return self._get("budgets")

    def get_autocomplete_accounts(self, limit=20):
        """Returns all user accounts."""
        acc_data = self.get_accounts(
            account_type=None, cache=True, pagination=True, limit=limit
        )
        account_names = FireflyAPI.process_accounts(
            acc_data, format="autocomplete", limit=limit
        )

        return account_names

    def create_transaction(self, transaction: Transaction):
        """Creates a new transaction.

        `Amount, Description, Source account, Destination account, Category, Budget`
        Example:
            - A simple one:
                -> `5, Large Mocha, Cash`
            - One with all the fields being used:
                -> `5, Large Mocha, Cash, Starbucks, Coffee Category, Food Budget`
            - You can skip specfic fields by leaving them empty (except the first two):
                -> `5, Large Mocha, Cash, , , UCO Bank`
        """

        payload = self.payload_formatter(transaction)

        return self._post(endpoint="transactions", payload=payload)

    def payload_formatter(self, transaction):
        trans_data = transaction.to_dict(remove_none=True, api_safe=True)
        header = {
            k.replace("header__", ""): v
            for k, v in trans_data.items()
            if k.startswith("header__")
        }
        body = {
            "transactions": [
                {k: v for k, v in trans_data.items() if not k.startswith("header__")}
            ]
        }
        return {**header, **body}

    @staticmethod
    def refresh_api(configs):
        FireflyAPI.flush_cache()
        return FireflyAPI(
            configs["firefly-cli"]["url"], configs["firefly-cli"]["api_token"]
        )

    @staticmethod
    def process_accounts(data, format="full", limit=9999):
        """Uses the same limit as the request"""

        accounts_proc = [] if format == "autocomplete" else {}

        break_outer = False
        for page in data:
            for acc in page["data"]:
                if (type(accounts_proc) == list and len(accounts_proc) == limit) or (
                    type(accounts_proc) == dict
                    and len(accounts_proc.setdefault("name", [])) == limit
                ):
                    break_outer = True
                    break
                if format == "autocomplete":

                    acc_fmt = acc["attributes"]["name"]
                    accounts_proc.append(acc_fmt)

                elif format == "full":

                    accounts_proc.setdefault("type", []).append(
                        acc["attributes"]["type"]
                    )
                    accounts_proc.setdefault("account_role", []).append(
                        acc["attributes"]["account_role"]
                    )
                    accounts_proc.setdefault("name", []).append(
                        acc["attributes"]["name"]
                    )
                    accounts_proc.setdefault("notes", []).append(
                        acc["attributes"]["notes"]
                    )
                    accounts_proc.setdefault("balance", []).append(
                        f"{acc['attributes']['currency_symbol']} {acc['attributes']['current_balance']}"
                    )
                    accounts_proc.setdefault("include_net_worth", []).append(
                        acc["attributes"]["include_net_worth"]
                    )

                else:
                    raise ValueError(
                        f"Format {format} is not valid for process_accounts"
                    )

            if break_outer:
                break

        return accounts_proc

    @staticmethod
    def count_total_page_elements(data):
        """Sums the total elements of "data" for all pages."""
        return sum(len(page["data"]) for page in data)

    @classmethod
    def flush_cache(cls):
        cls.rc.cache.clear()
