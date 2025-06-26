import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import CallableRaisesWarnsDeprecatedcall
from flake8_pytest_style.visitors import CallableRaisesWarnsDeprecatedcallVisitor


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="foo"):
                raise ValueError("foo")
            with pytest.warns(UserWarning, match="foo"):
                warnings.warn("foo", UserWarning)
            with pytest.deprecated_call():
                raise DeprecationWarning("foo")
    """
    assert_not_error(
        CallableRaisesWarnsDeprecatedcallVisitor, code, config=DEFAULT_CONFIG
    )


def test_error_raises():
    code = """
        import pytest

        def test_something():
            pytest.raises(ValueError, int, "notanumber")
    """
    assert_error(
        CallableRaisesWarnsDeprecatedcallVisitor,
        code,
        CallableRaisesWarnsDeprecatedcall,
        config=DEFAULT_CONFIG,
        name='raises',
    )


@pytest.mark.parametrize('api_name', ['warns', 'deprecated_call'])
def test_error_callable_forms(api_name: str):
    code = f"""
        import pytest
        import warnings

        def test_something():
            def my_raise_warning():
                warnings.warn(DeprecationWarning, "blah")
            pytest.{api_name}(my_raise_warning)
            """

    assert_error(
        CallableRaisesWarnsDeprecatedcallVisitor,
        code,
        CallableRaisesWarnsDeprecatedcall,
        config=DEFAULT_CONFIG,
        name=api_name,
    )
