import ast
import textwrap

import pytest
from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import (
    FixtureParamWithoutValue,
    TFunctionArgumentWithDefault,
)
from flake8_pytest_style.visitors import TFunctionsVisitor


def test_ok_good_param_name():
    code = """
        def test_xxx(fixture):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_non_test_function():
    code = """
        def xxx(_param):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_error_arg():
    code = """
        def test_xxx(_fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


def test_error_kwonly():
    code = """
        def test_xxx(*, _fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


@pytest.mark.parametrize("async_prefix", ["", "async "], ids=["sync", "async"])
@pytest.mark.parametrize(
    "names",
    [
        "'_value'",
        "' _value , expected '",
        "('_value', 'expected')",
        "['_value', 'expected']",
    ],
    ids=["string", "csv-whitespace", "tuple", "list"],
)
@pytest.mark.parametrize(
    "decorator",
    [
        "@pytest.mark.parametrize({names}, [1])",
        "@pytest.mark.parametrize(argnames={names}, argvalues=[1])",
    ],
    ids=["positional", "argnames-keyword"],
)
def test_ok_parametrized_underscore(async_prefix, names, decorator):
    code = f"""
        import pytest

        {decorator.format(names=names)}
        {async_prefix}def test_xxx(_value, expected):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("async_prefix", ["", "async "], ids=["sync", "async"])
@pytest.mark.parametrize("param_name", ["_set", "_value"])
@pytest.mark.parametrize("values", ["[(1, True)]", "generate()"])
def test_ok_parametrized_method(async_prefix, param_name, values):
    code = f"""
        import pytest

        class TestFoo:
            @pytest.mark.parametrize('{param_name},expected', {values})
            {async_prefix}def test_xxx(self, {param_name}: int, expected: bool) -> None:
                pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("async_prefix", ["", "async "], ids=["sync", "async"])
def test_ok_stacked_parametrize(async_prefix):
    code = f"""
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        @pytest.mark.parametrize('_other', [3, 4])
        {async_prefix}def test_xxx(_value, _other):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("async_prefix", ["", "async "], ids=["sync", "async"])
def test_ok_parametrized_kwonly(async_prefix):
    code = f"""
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        {async_prefix}def test_xxx(*, _value):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("async_prefix", ["", "async "], ids=["sync", "async"])
@pytest.mark.parametrize(
    "extra",
    [", ids=['a', 'b']", ", indirect=True", ", ids=['a', 'b'], indirect=True"],
)
def test_ok_parametrize_ids_or_indirect(async_prefix, extra):
    code = f"""
        import pytest

        @pytest.mark.parametrize('_value', [1, 2]{extra})
        {async_prefix}def test_xxx(_value):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_non_test_function_with_parametrize():
    code = """
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        def xxx(_value, _fixture):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_error_does_not_leak_between_functions():
    code = """
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        def test_ok(_value):
            pass

        def test_bad(_value):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_value")


def test_error_only_non_parametrized_underscore():
    code = """
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        def test_xxx(_value, _fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


def test_error_parametrize_different_name():
    code = """
        import pytest

        @pytest.mark.parametrize('value', [1, 2])
        def test_xxx(_value):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_value")


def test_error_location_is_function_def():
    code = textwrap.dedent("""
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        def test_xxx(_value, _fixture):
            pass
        """)
    tree = ast.parse(code)
    visitor = TFunctionsVisitor()
    visitor.visit(tree)
    func = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "test_xxx"
    )
    errors = [
        error for error in visitor.errors if isinstance(error, FixtureParamWithoutValue)
    ]
    assert len(errors) == 1
    assert errors[0].lineno == func.lineno
    assert errors[0].message == FixtureParamWithoutValue.formatted_message(
        name="_fixture"
    )


@pytest.mark.parametrize(
    "decorator",
    [
        "@pytest.mark.parametrize(NAMES, [1, 2])",
        "@pytest.mark.parametrize(f'{prefix}_value', [1, 2])",
        "@pytest.mark.parametrize('_value' + suffix, [1, 2])",
        "@pytest.mark.parametrize(argvalues=[1, 2])",
        "@pytest.mark.parametrize(1, [1, 2])",
        "@pytest.mark.parametrize(*ARGS)",
        "@pytest.mark.skip",
        "@other_decorator()",
        "@pytest.mark.parametrize('', [1])",
        "@pytest.mark.parametrize((), [1])",
        "@pytest.mark.parametrize([], [1])",
    ],
    ids=[
        "nonliteral",
        "f-string",
        "concat",
        "missing-argnames",
        "non-string-constant",
        "starred-call",
        "skip-decorator",
        "unrelated-decorator",
        "empty-string",
        "empty-tuple",
        "empty-list",
    ],
)
def test_error_unrecognized_parametrize_does_not_suppress(decorator):
    code = f"""
        import pytest

        {decorator}
        def test_xxx(_value):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_value")


def test_error_starred_name_elements_keep_literals():
    code = """
        import pytest

        @pytest.mark.parametrize(['_other', *MORE], [(1, 2)])
        def test_xxx(_value, _other):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_value")


def test_error_non_string_constant_in_sequence():
    code = """
        import pytest

        @pytest.mark.parametrize(('_other', 1), [(1, 2)])
        def test_xxx(_value, _other):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_value")


def test_error_parametrized_with_default_reports_pt028():
    code = """
        import pytest

        @pytest.mark.parametrize('_value', [1, 2])
        def test_xxx(_value=1):
            pass
    """
    visitor = TFunctionsVisitor()
    visitor.visit(ast.parse(textwrap.dedent(code)))
    assert not any(
        isinstance(error, FixtureParamWithoutValue) for error in visitor.errors
    )
    pt028_errors = [
        error
        for error in visitor.errors
        if isinstance(error, TFunctionArgumentWithDefault)
    ]
    assert len(pt028_errors) == 1
    assert pt028_errors[0].message == TFunctionArgumentWithDefault.formatted_message(
        name="test_xxx", arg="_value"
    )
