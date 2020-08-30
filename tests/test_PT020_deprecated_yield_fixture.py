from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import DeprecatedYieldFixture
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_no_parameters():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_without_parens():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            return 0
    """
    config = DEFAULT_CONFIG._replace(fixture_parentheses=False)
    assert_not_error(FixturesVisitor, code, config=config)


def test_error_without_parens():
    code = """
        import pytest

        @pytest.yield_fixture()
        def my_fixture():
            return 0
    """
    assert_error(FixturesVisitor, code, DeprecatedYieldFixture, config=DEFAULT_CONFIG)


def test_error_with_parens():
    code = """
        import pytest

        @pytest.yield_fixture
        def my_fixture():
            return 0
    """
    config = DEFAULT_CONFIG._replace(fixture_parentheses=False)
    assert_error(FixturesVisitor, code, DeprecatedYieldFixture, config=config)
