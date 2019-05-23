from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import MissingFixtureParentheses
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_no_parameters():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code)


def test_ok_with_parameters():
    code = """
        import pytest

        @pytest.fixture(scope='module')
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            return 0
    """
    assert_error(PytestStyleVisitor, code, MissingFixtureParentheses)
