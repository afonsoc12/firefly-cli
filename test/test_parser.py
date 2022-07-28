import json
from datetime import datetime
from pathlib import Path

import pytest

from firefly_cli import utils

test_data = Path(__file__).parent.joinpath("test_data")


class TestParser:
    def test_entrypoint(self):
        pass

    def test_accounts(self):
        pass

    def test_add(self):
        pass


class TestAutocomplete:
    def test_accounts_name_provider(self):
        pass

    def test_description_provider(self):
        pass
