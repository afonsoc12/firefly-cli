import json
import os
from datetime import date

import firefly_cli
from firefly_cli import FireflyPrompt
from firefly_cli.configs import load_configs
from firefly_cli.parser import Parser

from .utils import load_test_data, normalize, run_cmd


class TestFireflyPrompt:

    accounts_full = load_test_data("test_api", "api_accounts_full.json")
    transactions_response = load_test_data("test_api", "api_transactions_response.json")

    def test_format_version(self):
        fmt_version = FireflyPrompt.format_version()
        assert fmt_version.startswith("firefly-cli")
        assert fmt_version.split(": ")[-1] == firefly_cli.__version__

    def test_do_license(self, prompt):
        stdout, stderr = run_cmd(prompt, "license", skip_normalize=True)

        found_author, correct_year, correct_license = False, False, False
        for l in normalize(stdout, remove_empty=True):
            if not found_author and l.find("Copyright") > -1:
                found_author = True
            if not correct_year and l.find(str(date.today().year)) > -1:
                correct_year = True
            if not correct_license and l.find("Apache License") > -1:
                correct_license = True

        text_license = (
            True if len(normalize(stdout, remove_empty=True)[1:]) == 9 else False
        )

        assert found_author and correct_year and correct_license and text_license
        assert not stderr

    def test_help_license(self, prompt):
        stdout, stderr = run_cmd(prompt, "help license")
        assert stdout[0].find("Displays License information.") > -1
        assert not stderr

    def test_do_version(self, prompt):
        stdout, stderr = run_cmd(prompt, "version")
        assert (
            stdout[0].find("firefly-cli") > -1
            and stdout[0].find(firefly_cli.__version__) > -1
        )
        assert not stderr

    def test_help_version(self, prompt):
        stdout, stderr = run_cmd(prompt, "help version")
        assert stdout[0].find("Displays version information.") > -1
        assert not stderr

    def test_do_refresh(self, prompt):
        stdout, stderr = run_cmd(prompt, "refresh")
        assert stdout[0].find("API refreshed. Current Status:") > -1
        assert not stderr

    def test_help_refresh(self, prompt):
        stdout, stderr = run_cmd(prompt, "help refresh")
        assert stdout[0].find("Refreshes API connection.") > -1
        assert not stderr

    def test_do_edit(self, prompt, monkeypatch, tmp_path):

        # Load baseline config
        orig_location = os.environ["FIREFLY_CLI_CONFIG"]
        configs = load_configs()
        orig_url = configs["firefly-cli"]["url"]
        orig_api = configs["firefly-cli"]["api_token"]

        # Change config file
        new_url = "http://new.test.com"
        new_api = "new_api"
        tmp_file = tmp_path / "firefly-cli-test.ini"
        monkeypatch.setenv("FIREFLY_CLI_CONFIG", tmp_file)

        def mock_refresh_api(*args, **kwargs):
            return prompt.api

        monkeypatch.setattr(firefly_cli.api.FireflyAPI, "refresh_api", mock_refresh_api)

        # Edit URL
        stdout, stderr = run_cmd(prompt, f"edit url {new_url}")
        assert stdout[0].find("Config file saved at") > -1
        assert stdout[0].find(orig_location) == -1
        assert not stderr

        # Edit API
        stdout, stderr = run_cmd(prompt, f"edit api_token {new_api}")
        assert stdout[0].find("Config file saved at") > -1
        assert stdout[0].find(orig_location) == -1
        assert not stderr

        # Load and check the new file config
        configs = load_configs()
        assert (
            configs["firefly-cli"]["url"] == new_url
            and configs["firefly-cli"]["url"] != orig_url
        )
        assert (
            configs["firefly-cli"]["api_token"] == new_api
            and configs["firefly-cli"]["api_token"] != orig_api
        )

        # Load original file to check all was maintained
        os.environ["FIREFLY_CLI_CONFIG"] = orig_location
        configs = load_configs()
        assert (
            configs["firefly-cli"]["url"] == orig_url
            and configs["firefly-cli"]["url"] != new_url
        )
        assert (
            configs["firefly-cli"]["api_token"] == orig_api
            and configs["firefly-cli"]["api_token"] != new_api
        )

    def test_help_edit(self, prompt):
        stdout, stderr = run_cmd(prompt, "help edit")
        assert stdout[0].find("Edits connection credentials:") > -1
        assert stdout[1].startswith("\t> edit url")
        assert stdout[2].startswith("\t> edit api")
        assert not stderr

    def test_do_accounts(self, prompt):
        endpoint = "accounts"
        prompt.api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{prompt.api.api_url}{endpoint}?type=asset",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )
        stdout, stderr = run_cmd(prompt, "accounts")
        assert stdout[0].startswith("+---")
        assert len(stdout) == 47
        assert not stderr

    def test_do_accounts_json(self, prompt):
        endpoint = "accounts"
        prompt.api.rc.get_adapter("https://").register_uri(
            "GET",
            f"{prompt.api.api_url}{endpoint}?type=asset",
            headers={"Content-Type": "application/json"},
            json=self.accounts_full[0],
            status_code=200,
        )
        stdout, stderr = run_cmd(prompt, "accounts --json", skip_normalize=True)
        assert json.loads(stdout) == self.accounts_full
        assert not stderr

    def test_help_accounts(self, prompt):
        stdout, stderr = run_cmd(prompt, "help accounts", skip_normalize=True)
        assert stdout == Parser.accounts(prog="accounts").format_help()
        assert not stderr

    def test_do_budgets(self):
        # todo do_budgets
        pass

    def test_help_budgets(self, prompt):
        # todo help_budgets
        pass

    def test_do_add(self, prompt):
        endpoint = "transactions"
        prompt.api.rc.get_adapter("https://").register_uri(
            "POST",
            f"{prompt.api.api_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=self.transactions_response,
            status_code=200,
        )

        # Should error because will be stuck on y/n prompt
        stdout, stderr = run_cmd(
            prompt,
            "add 3, mocha, bank1  --date 1970-01-01 --destination-name expense3 --source-name bank",
            skip_normalize=True,
        )
        assert stderr.find("OSError") > -1
        assert stderr.find("pytest: reading from stdin while output is captured") > -1
        assert (
            stdout.find("Would you like to proceed adding the transaction? (y/n)") > -1
        )

        # Using -y will bypass prompt
        stdout, stderr = run_cmd(
            prompt,
            "add -y 3, mocha, bank1  --date 1970-01-01 --destination-name expense3 --source-name bank",
            skip_normalize=True,
        )
        stdout = normalize(stdout, remove_empty=True)

        assert stdout[0].find("Transaction header:") > -1
        assert stdout[4].find("True") > -1 and stdout[4].find("False") > -1
        assert stdout[6].find("Transaction body:") > -1
        assert (
            stdout[10].find("mocha") > -1
            and stdout[10].find(firefly_cli.__version__) > -1
        )
        assert stdout[-1].find("Transaction successfully added!") > -1
        assert not stderr

    def test_help_add(self, prompt):
        stdout, stderr = run_cmd(prompt, "help add", skip_normalize=True)
        assert stdout == Parser.add(prog="add").format_help()
        assert not stderr

    def test_do_exit(self, prompt):
        stdout, stderr = run_cmd(prompt, "exit")
        assert stdout[0].find("Bye! Come store new transactions soon!") > -1
        assert not stderr

    def test_help_exit(self, prompt):
        stdout, stderr = run_cmd(prompt, "help exit")
        assert stdout[0].find("Exits the application. Shorthand: q Ctrl-D.") > -1
        assert not stderr

    def test_default(self, prompt):
        # todo test default
        pass

    def test_do_q(self, prompt):
        stdout, stderr = run_cmd(prompt, "q")
        assert stdout[0].find("Bye! Come store new transactions soon!") > -1
        assert not stderr

    def test_help_q(self, prompt):
        stdout, stderr = run_cmd(prompt, "help q")
        assert stdout[0].find("Exits the application. Shorthand: q Ctrl-D.") > -1
        assert not stderr
