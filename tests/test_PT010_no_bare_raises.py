from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import NoBareRaises
from flake8_pytest_style.visitors import PytestStyleVisitor

CONFIG = Config(no_bare_raises_exceptions=['ValueError'])


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="Can't divide by 0"):
                raise ValueError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=CONFIG)


def test_ok_different_error_from_config():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ZeroDivisionError):
                raise ZeroDivisionError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=CONFIG)


def test_error_no_argument_given():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises, config=CONFIG)


def test_error_match_is_none():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError, match=None):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises, config=CONFIG)
