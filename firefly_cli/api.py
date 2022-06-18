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

    def __init__(self, hostname, auth_token):
        self.headers = {"Authorization": "Bearer " + auth_token if auth_token else ""}
        self.hostname = (
            hostname
            if hostname is None or not hostname.endswith("/")
            else hostname[:-1]
        )  # Remove trailing backslash
        self.hostname = self.hostname + "/api/v1/" if hostname else self.hostname
        self.api_test = self._test_api()

    def _test_api(self):
        """Tests API connection."""
        try:
            _ = self.get_about_user()
            return True
        except:
            return False

    def _post(self, endpoint, payload):
        """Handles general POST requests."""

        response = self.rc.post(
            "{}{}".format(self.hostname, endpoint),
            json=payload,
            # Pass extra headers, or it redirects to login
            headers={
                **self.headers,
                **{"Content-Type": "application/json", "accept": "application/json"},
            },
        )

        return response

    def _get(self, endpoint, params={}, cache=False, pagination=False):
        """Handles general GET requests."""

        responses = []
        with self.rc.cache_disabled() if not cache else nullcontext():
            response = self.rc.get(
                "{}{}".format(self.hostname, endpoint),
                params=params,
                headers=self.headers,
            )

        responses.append(response.json())

        if pagination:
            while "next" in response.json()["links"]:
                params["page"] = (
                    response.json()["meta"]["pagination"]["current_page"] + 1
                )
                with self.rc.cache_disabled() if not cache else nullcontext():
                    response = self.rc.get(
                        "{}{}".format(self.hostname, endpoint),
                        params=params,
                        headers=self.headers,
                    )

                responses.append(response.json())

        return responses

    def get_budgets(self):
        """Returns budgets of the user."""

        return self._get("budgets")

    def get_accounts(self, account_type="asset", cache=False, pagination=False):
        """Returns all user accounts."""
        params = {"type": account_type} if account_type else {}

        return self._get("accounts", params=params, cache=cache, pagination=pagination)

    def get_autocomplete_accounts(self):
        """Returns all user accounts."""
        acc_data = self.get_accounts(account_type=None, cache=True, pagination=True)
        account_names = FireflyAPI.process_accounts(acc_data, format='autocomplete')

        return account_names

    def get_about_user(self):
        """Returns user information."""

        return self._get("about/user")

    def create_transaction(self, transaction: Transaction):
        """Creates a new transaction.
        data:
            pd.DataFrame

        `Amount, Description, Source account, Destination account, Category, Budget`
        Example:
            - A simple one:
                -> `5, Large Mocha, Cash`
            - One with all the fields being used:
                -> `5, Large Mocha, Cash, Starbucks, Coffee Category, Food Budget`
            - You can skip specfic fields by leaving them empty (except the first two):
                -> `5, Large Mocha, Cash, , , UCO Bank`
        """

        trans_data = transaction.to_dict(remove_none=True, api_safe=True)

        header = {k: v for k, v in trans_data.items() if k.startswith("header__")}
        body = {
            "transactions": [
                {k: v for k, v in trans_data.items() if not k.startswith("header__")}
            ]
        }

        payload = {**header, **body}

        return self._post(endpoint="transactions", payload=payload)

    @staticmethod
    def process_accounts(data, format="full"):

        accounts_proc = [] if format == "autocomplete" else {}

        for page in data:
            for acc in page["data"]:
                if format == "autocomplete":

                    acc_fmt = acc['attributes']['name']
                    acc_fmt += f" ({acc['attributes']['currency_symbol']}{acc['attributes']['current_balance']})" if acc['attributes']['type'] == 'asset' else ""
                    accounts_proc.append(acc_fmt)

                elif format == "full":

                    accounts_proc.setdefault("type", []).append(acc["attributes"]["type"])
                    accounts_proc.setdefault("account_role", []).append(acc["attributes"]["account_role"])
                    accounts_proc.setdefault("name", []).append(acc["attributes"]["name"])
                    accounts_proc.setdefault("notes", []).append(acc["attributes"]["notes"])
                    accounts_proc.setdefault("balance", []).append(f"{acc['attributes']['currency_symbol']} {acc['attributes']['current_balance']}")
                    accounts_proc.setdefault("include_net_worth", []).append(acc["attributes"]["include_net_worth"])

                else:
                    raise ValueError(f"Format {format} is not valid for process_accounts")


        return accounts_proc

    @classmethod
    def flush_cache(cls):
        cls.rc.cache.clear()
