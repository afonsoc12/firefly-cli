import pytest
from requests_cache import CachedSession
from requests_mock import Adapter

from firefly_cli import FireflyAPI, FireflyPrompt
from firefly_cli.configs import load_configs


@pytest.fixture
def api(configs):
    """Fixture that provides a CachedSession that will make mock requests where it would normally
    make real requests"""
    api = FireflyAPI(
        hostname=configs["firefly-cli"]["url"],
        auth_token=configs["firefly-cli"]["api_token"],
        check_connection=False,
    )

    adapter = Adapter()

    session = CachedSession(backend="memory")
    session.mount("https://", adapter)

    api.rc = session

    yield api


@pytest.fixture
def prompt(api):
    prompt = FireflyPrompt()
    prompt.api = api
    return prompt


@pytest.fixture
def configs():
    return load_configs()
