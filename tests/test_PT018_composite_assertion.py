import pytest
from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import CompositeAssertion
from flake8_pytest_style.visitors.assertion import AssertionVisitor


def test_ok():
    code = """
        def test_xxx():
            assert something
            assert something or something_else
            assert something or something_else and something_third
            assert not (something and something_else)
    """
    assert_not_error(AssertionVisitor, code)


@pytest.mark.parametrize(
    'condition',
    [
        'something and something_else',
        'something and something_else and something_third',
        'something and not something_else',
        'something and (something_else or something_third)',
        'not (something or something_else)',
        'not (something or something_else or something_third)',
        'not (something or something_else and something_third)',
    ],
)
def test_error(condition):
    code = f"""
        def test_xxx():
            assert {condition}
    """
    assert_error(AssertionVisitor, code, CompositeAssertion)
