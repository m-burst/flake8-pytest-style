import ast
from typing import List, Union

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    ExtraneousScopeFunction,
    FixtureFinalizerCallback,
    FixtureParamWithoutValue,
    FixturePositionalArgs,
    IncorrectFixtureNameUnderscore,
    IncorrectFixtureParenthesesStyle,
    MissingFixtureNameUnderscore,
    YieldFixture,
)
from flake8_pytest_style.utils import (
    AnyFunctionDef,
    get_all_argument_names,
    get_fixture_decorator,
    get_qualname,
    is_pytest_yield_fixture,
    is_test_function,
)


class _AddFinalizerVisitor(ast.NodeVisitor):
    """
    Helper AST visitor to find request.addfinalizer in fixtures.

    Does not descend into nested functions.

    Main entrypoint is the `search` method.
    """

    root: ast.AST

    def __init__(self) -> None:
        self._found: List[ast.AST] = []

    def search(self, node: AnyFunctionDef) -> List[ast.AST]:
        self._found = []
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        return self._found

    def visit_FunctionDef(self, node: AnyFunctionDef) -> None:
        # do not descend into nested functions
        pass

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815

    def visit_Call(self, node: ast.Call) -> None:
        if get_qualname(node.func) == 'request.addfinalizer':
            self._found.append(node)


class FixturesVisitor(Visitor[Config]):
    def _check_fixture_decorator_name(
        self, fixture_decorator: Union[ast.Call, ast.Attribute]
    ) -> None:
        """Checks for PT020."""
        if isinstance(fixture_decorator, ast.Call):
            is_yield = is_pytest_yield_fixture(fixture_decorator.func)
        else:
            is_yield = is_pytest_yield_fixture(fixture_decorator)
        if is_yield:
            self.error_from_node(YieldFixture, fixture_decorator)

    def _check_fixture_decorator(
        self,
        fixture_decorator: Union[ast.Call, ast.Attribute],
        fixture_func: AnyFunctionDef,
    ) -> None:
        """Checks for PT001, PT002, PT003."""
        if not isinstance(fixture_decorator, ast.Call):
            if self.config.fixture_parentheses:
                self.error_from_node(
                    IncorrectFixtureParenthesesStyle,
                    fixture_decorator,
                    expected_parens='()',
                    actual_parens='',
                )
            return

        if (
            not self.config.fixture_parentheses
            and not fixture_decorator.args
            and not fixture_decorator.keywords
        ):
            self.error_from_node(
                IncorrectFixtureParenthesesStyle,
                fixture_decorator,
                expected_parens='',
                actual_parens='()',
            )

        if fixture_decorator.args:
            self.error_from_node(
                FixturePositionalArgs, fixture_decorator, name=fixture_func.name
            )

        for keyword in fixture_decorator.keywords:
            if (
                keyword.arg == 'scope'
                and isinstance(keyword.value, ast.Str)
                and keyword.value.s == 'function'
            ):
                self.error_from_node(
                    ExtraneousScopeFunction, fixture_decorator, name=fixture_func.name
                )

    def _check_fixture_returns(self, node: AnyFunctionDef) -> None:
        """Checks for PT004, PT005."""
        has_return_with_value = False
        for child in ast.walk(node):
            if isinstance(child, (ast.Return, ast.Yield)) and child.value is not None:
                has_return_with_value = True
                break

        if has_return_with_value and node.name.startswith('_'):
            self.error_from_node(IncorrectFixtureNameUnderscore, node, name=node.name)
        elif not has_return_with_value and not node.name.startswith('_'):
            self.error_from_node(MissingFixtureNameUnderscore, node, name=node.name)

    def _check_fixture_addfinalizer(self, node: AnyFunctionDef) -> None:
        """Checks for PT021."""
        if 'request' not in get_all_argument_names(node.args):
            return

        visitor = _AddFinalizerVisitor()
        found = visitor.search(node)
        if found:
            self.error_from_node(FixtureFinalizerCallback, found[0])

    def _check_test_function_args(self, node: AnyFunctionDef) -> None:
        """Checks for PT019."""
        # intentionally not looking at posonlyargs because pytest passes everything
        # as kwargs, so declaring fixture args as positional-only will fail anyway
        for arg in node.args.args + node.args.kwonlyargs:
            if arg.arg.startswith('_'):
                self.error_from_node(FixtureParamWithoutValue, node, name=arg.arg)

    def visit_FunctionDef(self, node: AnyFunctionDef) -> None:
        fixture_decorator = get_fixture_decorator(node)
        if fixture_decorator:
            self._check_fixture_decorator_name(fixture_decorator)
            self._check_fixture_decorator(fixture_decorator, node)
            self._check_fixture_returns(node)
            self._check_fixture_addfinalizer(node)

        if is_test_function(node):
            self._check_test_function_args(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815
