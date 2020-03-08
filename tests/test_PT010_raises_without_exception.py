from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import RaisesWithoutException
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(UnicodeError):
                pass
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_error():
    code = """
        import pytest

        def test_something():
            with pytest.raises():
                pass
    """
    assert_error(
        PytestStyleVisitor, code, RaisesWithoutException, config=DEFAULT_CONFIG
    )
