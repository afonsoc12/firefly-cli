import test.utils as test
from datetime import datetime

import pytest

from firefly_cli import utils


class TestUtils:

    test_data = test.load_test_data(__name__, "test_data.json")

    @pytest.mark.parametrize(
        "ans, expected",
        [
            (
                "y",
                True,
            ),
            (
                "Y",
                True,
            ),
            (
                "yes",
                True,
            ),
            (
                "Yes",
                True,
            ),
            (
                "YES",
                True,
            ),
            (
                "n",
                False,
            ),
            (
                "abc",
                False,
            ),
            (
                "",
                False,
            ),
        ],
    )
    def test_prompt_continue(self, monkeypatch, ans, expected):
        """Asserts if user input returns expected."""
        monkeypatch.setattr("builtins.input", lambda _: ans)
        assert utils.prompt_continue() == expected

    @pytest.mark.parametrize(
        "dt",
        [
            datetime(2022, 2, 1),
            datetime(2022, 2, 1, 0, 0, 0),
            datetime(2022, 2, 1).astimezone(),
            datetime(2022, 2, 1, 0, 0, 0).astimezone(),
        ],
    )
    def test_json_serial(self, dt):
        """Asserts if datetimes are correctly serialzed as json objects."""
        dt_expected = datetime(2022, 2, 1, 0, 0, 0)
        if dt.tzinfo:
            dt_expected = dt_expected.astimezone()

        assert utils.json_serial(dt, iso_format=True) == dt_expected.isoformat()
        assert utils.json_serial(dt, iso_format=False) == dt_expected.strftime(
            "%a, %Y-%m-%d %H:%M:%S"
        )

    def test_json_serial_error(self):
        dt = "2020-02-01"
        with pytest.raises(TypeError):
            utils.json_serial(dt, iso_format=True)
            utils.json_serial(dt, iso_format=False)

    def test_date_to_datetime(self):
        dt = "2022-02-01"
        assert utils.date_to_datetime(dt) == datetime(2022, 2, 1).astimezone()

    def test_datetime_to_datetime(self):
        dt = "2022-02-01T01:02:03"
        assert (
            utils.datetime_to_datetime(dt) == datetime(2022, 2, 1, 1, 2, 3).astimezone()
        )

    def test_tabulate(self):
        input = self.test_data["test_tabulate"]["data"]
        output = self.test_data["test_tabulate"]["expected"]

        assert utils.tabulate(input) == output[0]
        assert utils.tabulate(input, header_fmt="capitalise_from_snake") == output[1]

    @pytest.mark.parametrize(
        "s, expected, expected_capitalise",
        [
            ("a_string", "a string", "A String"),
            ("a", "a", "A"),
            (
                "a A",
                "a A",
                "A a",
            ),
            ("trailing_", "trailing", "Trailing"),
        ],
    )
    def test_snake_to_spaced(self, s, expected, expected_capitalise):
        assert utils.snake_to_spaced(s) == expected
        assert utils.snake_to_spaced(s, capitalise=True) == expected_capitalise
