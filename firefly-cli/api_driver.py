import requests
import datetime

"""FireflyIII API Driver.
Created by: @vjFaLk
Enhanced by: @afonsoc12

API documentation: https://api-docs.firefly-iii.org
"""


class FireflyAPI:
    """Firefly API driver Class."""

    def __init__(self, hostname, auth_token):
        self.headers = {'Authorization': "Bearer " + auth_token if auth_token is not None else ''}
        self.hostname = hostname if hostname is None or not hostname.endswith('/') else hostname[:-1]  # Remove trailing backslash
        self.hostname = self.hostname + '/api/v1/' if hostname is not None else self.hostname
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

        return requests.post("{}{}".format(self.hostname, endpoint), json=payload, headers=self.headers)

    def _get(self, endpoint, params=None):
        """Handles general GET requests."""

        response = requests.get("{}{}".format(
            self.hostname, endpoint), params=params, headers=self.headers)
        return response.json()

    def get_budgets(self):
        """Returns budgets of the user."""

        return self._get("budgets")

    def get_accounts(self, account_type="asset"):
        """Returns all user accounts."""

        return self._get("accounts", params={"type": account_type})

    def get_about_user(self):
        """Returns user information."""

        return self._get("about/user")

    def create_transaction(self, amount, description, source_account, destination_account=None, category=None,
                           budget=None):
        """Creates a new transaction."""

        now = datetime.datetime.now()
        payload = {
            "transactions": [{
                "type": "withdrawal",
                "description": description,
                "date": now.strftime("%Y-%m-%d"),
                "amount": amount,
                "budget_name": budget,
                "category_name": category,
            }]
        }
        if source_account.isnumeric():
            payload["transactions"][0]["source_id"] = source_account
        else:
            payload["transactions"][0]["source_name"] = source_account

        if destination_account:
            if destination_account.isnumeric():
                payload["transactions"][0]["destination_id"] = destination_account
            else:
                payload["transactions"][0]["destination_name"] = destination_account
        else:
            payload["transactions"][0]["destination_name"] = description

        return self._post(endpoint="transactions", payload=payload)
