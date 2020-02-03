from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import NoBareRaises
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="Can't divide by 0"):
                raise ValueError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error_no_argument_given():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises)


def test_error_match_is_none():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError, match=None):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises)
