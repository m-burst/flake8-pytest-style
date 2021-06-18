from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import UseFixturesWithoutParameters
from flake8_pytest_style.visitors import MarksVisitor


def test_ok():
    code = """
        import pytest

        @pytest.mark.usefixtures('a')
        def test_something():
            pass
    """
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_another_mark_with_parens():
    code = """
        import pytest

        @pytest.mark.foo()
        def test_something():
            pass
    """
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_another_mark_no_parens():
    code = """
        import pytest

        @pytest.mark.foo
        def test_something():
            pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_not_error(MarksVisitor, code, config=config)


def test_error_with_parens():
    code = """
        import pytest

        @pytest.mark.usefixtures()
        def test_something():
            pass
    """
    assert_error(
        MarksVisitor, code, UseFixturesWithoutParameters, config=DEFAULT_CONFIG
    )


def test_error_no_parens():
    code = """
        import pytest

        @pytest.mark.usefixtures
        def test_something():
            pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_error(MarksVisitor, code, UseFixturesWithoutParameters, config=config)
