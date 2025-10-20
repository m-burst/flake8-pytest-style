import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import WarnsTooBroad
from flake8_pytest_style.visitors import WarnsVisitor


def test_ok():
    code = """
        import pytest
        import warnings

        def test_something():
            with pytest.warns(UserWarning, match="foo"):
                warnings.warn("foo", UserWarning)
    """
    assert_not_error(WarnsVisitor, code, config=DEFAULT_CONFIG)


def test_ok_different_error_from_config():
    code = """
        import pytest
        import warnings

        def test_something():
            with pytest.warns(BytesWarning):
                warnings.warn("foo", UserWarning)
    """
    assert_not_error(WarnsVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize("warning", ["Warning", "UserWarning"])
def test_error_no_argument_given(warning):
    code = f"""
        import pytest
        import warnings

        def test_something():
            with pytest.warns({warning}):
                warnings.warn("foo", UserWarning)
    """
    assert_error(
        WarnsVisitor,
        code,
        WarnsTooBroad,
        config=DEFAULT_CONFIG,
        warning=warning,
    )


@pytest.mark.parametrize("match", ["None", '""', 'f""'])
def test_error_match_is_empty(match):
    code = f"""
        import pytest
        import warnings

        def test_something():
            with pytest.warns(UserWarning, match={match}):
                warnings.warn("foo", UserWarning)
    """
    assert_error(
        WarnsVisitor,
        code,
        WarnsTooBroad,
        config=DEFAULT_CONFIG,
        warning="UserWarning",
    )
