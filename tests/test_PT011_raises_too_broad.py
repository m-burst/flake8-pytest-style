import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import RaisesTooBroad
from flake8_pytest_style.visitors import RaisesVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="Can't divide by 0"):
                raise ValueError("Can't divide by 0")
    """
    assert_not_error(RaisesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_different_error_from_config():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ZeroDivisionError):
                raise ZeroDivisionError("Can't divide by 0")
    """
    assert_not_error(RaisesVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize('exception', ['ValueError', 'socket.error'])
def test_error_no_argument_given(exception):
    code = f"""
        import pytest

        def test_something():
            with pytest.raises({exception}):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(
        RaisesVisitor,
        code,
        RaisesTooBroad,
        config=DEFAULT_CONFIG,
        exception=exception,
    )


@pytest.mark.parametrize('match', ['None', '""', 'f""'])
def test_error_match_is_empty(match):
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError, match={match}):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(
        RaisesVisitor,
        code,
        RaisesTooBroad,
        config=DEFAULT_CONFIG,
        exception='ValueError',
    )
