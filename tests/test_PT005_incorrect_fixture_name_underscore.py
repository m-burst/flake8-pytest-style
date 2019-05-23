from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import IncorrectFixtureNameUnderscore
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture(mocker):
            return 0
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error():
    code = """
        import pytest

        @pytest.fixture()
        def _my_fixture(mocker):
            return 0
    """
    assert_error(
        PytestStyleVisitor, code, IncorrectFixtureNameUnderscore, name='_my_fixture'
    )
