import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import RaisesWithMultipleStatements
from flake8_pytest_style.visitors import RaisesVisitor


def test_ok():
    code = """
        def test_something():
            with pytest.raises(AttributeError):
                [].size
    """
    assert_not_error(RaisesVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize("maybe_async", ["", "async "])
def test_ok_trivial_with(maybe_async):
    code = f"""
        async def test_something():
            with pytest.raises(AttributeError):
                {maybe_async}with context_manager_under_test():
                    pass
    """
    assert_not_error(RaisesVisitor, code, config=DEFAULT_CONFIG)


def test_error_multiple_statements():
    code = """
        def test_something():
            with pytest.raises(AttributeError):
                len([])
                [].size
    """
    assert_error(
        RaisesVisitor, code, RaisesWithMultipleStatements, config=DEFAULT_CONFIG
    )


@pytest.mark.parametrize(
    "statement", ["if", "for i in", "async for i in", "while", "with", "async with"]
)
def test_error_complex_statement(statement):
    code = f"""
        async def test_something():
            with pytest.raises(AttributeError):
                {statement} True:
                    [].size
    """
    assert_error(
        RaisesVisitor, code, RaisesWithMultipleStatements, config=DEFAULT_CONFIG
    )


def test_error_try():
    code = """
        def test_something():
            with pytest.raises(AttributeError):
                try:
                    [].size
                except:
                    raise
    """
    assert_error(
        RaisesVisitor, code, RaisesWithMultipleStatements, config=DEFAULT_CONFIG
    )
