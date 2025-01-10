import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import WarnsWithMultipleStatements
from flake8_pytest_style.visitors import WarnsVisitor


def test_ok():
    code = """
        def test_something():
            with pytest.warns(BytesWarning):
                [].size
    """
    assert_not_error(WarnsVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize('maybe_async', ['', 'async '])
def test_ok_trivial_with(maybe_async):
    code = f"""
        async def test_something():
            with pytest.warns(BytesWarning):
                {maybe_async}with context_manager_under_test():
                    pass
    """
    assert_not_error(WarnsVisitor, code, config=DEFAULT_CONFIG)


def test_error_multiple_statements():
    code = """
        def test_something():
            with pytest.warns(BytesWarning):
                len([])
                [].size
    """
    assert_error(WarnsVisitor, code, WarnsWithMultipleStatements, config=DEFAULT_CONFIG)


@pytest.mark.parametrize(
    'statement', ['if', 'for i in', 'async for i in', 'while', 'with', 'async with']
)
def test_error_complex_statement(statement):
    code = f"""
        async def test_something():
            with pytest.warns(BytesWarning):
                {statement} True:
                    [].size
    """
    assert_error(WarnsVisitor, code, WarnsWithMultipleStatements, config=DEFAULT_CONFIG)


def test_error_try():
    code = """
        def test_something():
            with pytest.warns(BytesWarning):
                try:
                    [].size
                except:
                    raise
    """
    assert_error(WarnsVisitor, code, WarnsWithMultipleStatements, config=DEFAULT_CONFIG)
