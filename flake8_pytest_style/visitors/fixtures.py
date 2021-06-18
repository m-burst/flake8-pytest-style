import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    DeprecatedYieldFixture,
    ErroneousUseFixturesOnFixture,
    ExtraneousScopeFunction,
    FixtureFinalizerCallback,
    FixtureParamWithoutValue,
    FixturePositionalArgs,
    IncorrectFixtureNameUnderscore,
    IncorrectFixtureParenthesesStyle,
    MissingFixtureNameUnderscore,
    UnnecessaryAsyncioMarkOnFixture,
    UselessYieldFixture,
)
from flake8_pytest_style.utils import (
    AnyFunctionDef,
    get_all_argument_names,
    get_fixture_decorator,
    get_mark_decorators,
    get_mark_name,
    get_qualname,
    is_abstract_method,
    is_pytest_yield_fixture,
    is_test_function,
    walk_without_nested_functions,
)


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
            self.error_from_node(DeprecatedYieldFixture, fixture_decorator)

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
        """Checks for PT004, PT005, PT022."""
        # skip these checks for abstract fixtures
        if is_abstract_method(node):
            return

        has_return_with_value = False
        has_yield_from = False
        yield_statements = []
        for child in walk_without_nested_functions(node):
            if isinstance(child, ast.Yield):
                yield_statements.append(child)
            if isinstance(child, (ast.Return, ast.Yield)) and child.value is not None:
                has_return_with_value = True
            if isinstance(child, ast.YieldFrom):
                has_yield_from = True

        if has_return_with_value and node.name.startswith('_'):
            self.error_from_node(IncorrectFixtureNameUnderscore, node, name=node.name)
        elif (
            not has_return_with_value
            and not has_yield_from
            and not node.name.startswith('_')
        ):
            # we shouldn't fire PT004 if we found a `yield from` because
            # there is no adequate way to determine whether a value is actually yielded
            self.error_from_node(MissingFixtureNameUnderscore, node, name=node.name)

        last_statement_is_yield = isinstance(node.body[-1], ast.Expr) and isinstance(
            node.body[-1].value, ast.Yield
        )
        if last_statement_is_yield and len(yield_statements) == 1:
            self.error_from_node(UselessYieldFixture, node, name=node.name)

    def _check_fixture_addfinalizer(self, node: AnyFunctionDef) -> None:
        """Checks for PT021."""
        if 'request' not in get_all_argument_names(node.args):
            return

        for child in walk_without_nested_functions(node):  # pragma: no branch
            if (
                isinstance(child, ast.Call)
                and get_qualname(child.func) == 'request.addfinalizer'
            ):
                self.error_from_node(FixtureFinalizerCallback, child)
                return

    def _check_fixture_marks(self, node: AnyFunctionDef) -> None:
        """Checks for PT024, PT025."""
        reported_errors = set()
        marks = get_mark_decorators(node)
        for mark in marks:
            mark_name = get_mark_name(mark)
            if (
                mark_name == 'asyncio'
                and UnnecessaryAsyncioMarkOnFixture not in reported_errors
            ):
                self.error_from_node(UnnecessaryAsyncioMarkOnFixture, mark)
                reported_errors.add(UnnecessaryAsyncioMarkOnFixture)
            if (
                mark_name == 'usefixtures'
                and ErroneousUseFixturesOnFixture not in reported_errors
            ):
                self.error_from_node(ErroneousUseFixturesOnFixture, mark)
                reported_errors.add(ErroneousUseFixturesOnFixture)

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
            self._check_fixture_marks(node)

        if is_test_function(node):
            self._check_test_function_args(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815
