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

        response = requests.post("{}{}".format(self.hostname, endpoint),
                             json=payload,
                             # Pass extra headers, or it redirects to login
                             headers={**self.headers,
                                      **{'Content-Type': 'application/json',
                                         'accept': 'application/json'}
                                      }
                             )

        return response

    def _get(self, endpoint, params=None):
        """Handles general GET requests."""

        response = requests.get("{}{}".format(self.hostname, endpoint),
                                params=params,
                                headers=self.headers)

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

    def create_transaction(self, data):
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

        # TODO : Allow DataFrames bigger than 1
        i = 0

        payload = {
            "transactions": [{
                "type": "withdrawal",
                "description": data['description'].iloc[0],
                "date": data.index[i].strftime("%Y-%m-%d"),
                "amount": float(data['amount'].iloc[0]),
                "budget_name": data['budget'].iloc[0],
                "category_name": data['category'].iloc[0],
            }]
        }
        if data['source_name'].iloc[0].isnumeric():
            payload["transactions"][0]["source_id"] = data['source_name'].iloc[0]
        else:
            payload["transactions"][0]["source_name"] = data['source_name'].iloc[0]

        if data['destination_name'].iloc[0] is not None:
            if data['destination_name'].iloc[0].isnumeric():
                payload["transactions"][0]["destination_id"] = data['destination_name'].iloc[0]
            else:
                payload["transactions"][0]["destination_name"] = data['destination_name'].iloc[0]
        else:
            payload["transactions"][0]["destination_name"] = data['description'].iloc[0]

        return self._post(endpoint="transactions", payload=payload)
