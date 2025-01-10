import ast
import textwrap

from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import TFunctionArgumentWithDefault
from flake8_pytest_style.visitors import TFunctionsVisitor


def test_ok():
    code = """
        def test_xxx(fixture1, /, fixture2, *, fixture3):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_non_test_function():
    code = """
        def xxx(posonly1, posonly2=2, /, arg=3, *, kwonly=4):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_error_posonly():
    code = """
        def test_xxx(posonly1, posonly2=2, /):
            pass
    """
    assert_error(
        TFunctionsVisitor,
        code,
        TFunctionArgumentWithDefault,
        name='test_xxx',
        arg='posonly2',
    )


def test_error_arg():
    code = """
        def test_xxx(arg1, arg2=2):
            pass
    """
    assert_error(
        TFunctionsVisitor,
        code,
        TFunctionArgumentWithDefault,
        name='test_xxx',
        arg='arg2',
    )


def test_error_kwonly():
    code = """
        def test_xxx(*, kwonly1, kwonly2=2):
            pass
    """
    assert_error(
        TFunctionsVisitor,
        code,
        TFunctionArgumentWithDefault,
        name='test_xxx',
        arg='kwonly2',
    )


def test_error_multiple():
    code = """
        def test_xxx(
            posonly=1,
            /,
            arg=2,
            *,
            kwonly=3,
        ):
            pass
    """
    # flake8-plugin-utils does not allow multiple errors in a single test
    visitor = TFunctionsVisitor()
    visitor.visit(ast.parse(textwrap.dedent(code)))
    assert len(visitor.errors) == 3
    posonly_error, arg_error, kwonly_error = visitor.errors

    assert isinstance(posonly_error, TFunctionArgumentWithDefault)
    assert posonly_error.message == TFunctionArgumentWithDefault.formatted_message(
        name='test_xxx', arg='posonly'
    )
    assert posonly_error.lineno == 3

    assert isinstance(arg_error, TFunctionArgumentWithDefault)
    assert arg_error.message == TFunctionArgumentWithDefault.formatted_message(
        name='test_xxx', arg='arg'
    )
    assert arg_error.lineno == 5

    assert isinstance(kwonly_error, TFunctionArgumentWithDefault)
    assert kwonly_error.message == TFunctionArgumentWithDefault.formatted_message(
        name='test_xxx', arg='kwonly'
    )
    assert kwonly_error.lineno == 7
