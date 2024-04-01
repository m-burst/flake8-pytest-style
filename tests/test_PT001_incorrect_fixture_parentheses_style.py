from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import IncorrectFixtureParenthesesStyle
from flake8_pytest_style.visitors import FixturesVisitor

# make the configs independent of the actual default
_CONFIG_WITHOUT_PARENS = DEFAULT_CONFIG._replace(fixture_parentheses=False)
_CONFIG_WITH_PARENS = DEFAULT_CONFIG._replace(fixture_parentheses=True)


def test_ok_no_parameters():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=_CONFIG_WITH_PARENS)


def test_ok_with_parameters():
    code = """
        import pytest

        @pytest.fixture(scope='module')
        def my_fixture():
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=_CONFIG_WITH_PARENS)


def test_ok_without_parens():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=_CONFIG_WITHOUT_PARENS)


def test_error_without_parens():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureParenthesesStyle,
        config=_CONFIG_WITH_PARENS,
        expected_parens='()',
        actual_parens='',
    )


def test_error_with_parens():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureParenthesesStyle,
        config=_CONFIG_WITHOUT_PARENS,
        expected_parens='',
        actual_parens='()',
    )
