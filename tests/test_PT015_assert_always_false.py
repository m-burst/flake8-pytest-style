import pytest
from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import AssertAlwaysFalse
from flake8_pytest_style.visitors import FailVisitor


def test_ok():
    code = """
        def test_xxx():
            assert [0]
    """
    assert_not_error(FailVisitor, code)


@pytest.mark.parametrize(
    "falsy_constant",
    [
        "None",
        "False",
        "0",
        "0.0",
        '""',
        'f""',
        "[]",
        "()",
        "{}",
        "list()",
        "set()",
        "tuple()",
        "dict()",
        "frozenset()",
        "list([])",
        "set(set())",
        'tuple("")',
    ],
)
def test_error(falsy_constant):
    code = f"""
        def test_xxx():
            assert {falsy_constant}
    """
    assert_error(FailVisitor, code, AssertAlwaysFalse)
