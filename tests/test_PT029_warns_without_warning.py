from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import WarnsWithoutException
from flake8_pytest_style.visitors import WarnsVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.warns(UnicodeError):
                pass
    """
    assert_not_error(WarnsVisitor, code, config=DEFAULT_CONFIG)


def test_error():
    code = """
        import pytest

        def test_something():
            with pytest.warns():
                pass
    """
    assert_error(WarnsVisitor, code, WarnsWithoutException, config=DEFAULT_CONFIG)
