import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import RaisesWithoutMatch
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="Can't divide by 0"):
                raise ValueError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_ok_different_error_from_config():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ZeroDivisionError):
                raise ZeroDivisionError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize('exception', ['ValueError', 'socket.error'])
def test_error_no_argument_given(exception):
    code = f"""
        import pytest

        def test_something():
            with pytest.raises({exception}):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(
        PytestStyleVisitor,
        code,
        RaisesWithoutMatch,
        config=DEFAULT_CONFIG,
        exception=exception,
    )


def test_error_match_is_none():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match=None):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(
        PytestStyleVisitor,
        code,
        RaisesWithoutMatch,
        config=DEFAULT_CONFIG,
        exception='ValueError',
    )
