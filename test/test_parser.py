import shlex
import sys
from unittest.mock import patch

from firefly_cli.parser import Parser


class TestAutocomplete:
    def test_accounts_name_provider(self):
        pass

    def test_description_provider(self):
        pass


class TestParser:
    def test_entrypoint(self):
        pass

    def test_accounts(self):
        pass

    def test_add(self):
        pass

    def test_safe_string(self):
        test_argv = [
            "script.py",
            "add",
            "--source-name",
            "My Bank Account",
            "--amount",
            "499",
            "--description",
            "Food",
            "--destination-name",
            "Shop A",
        ]
        expected_args_str = "add --source-name 'My Bank Account' --amount 499 --description Food --destination-name 'Shop A'"

        with patch.object(sys, "argv", test_argv):
            args, ffargs = Parser.entrypoint().parse_known_args()

        args_str = Parser.safe_string(ffargs)
        args = Parser.add().parse_args(shlex.split(args_str))

        assert args_str == expected_args_str
        assert args.source_name == "My Bank Account"
        assert args.amount == 499
        assert args.description == "Food"
        assert args.destination_name == "Shop A"
