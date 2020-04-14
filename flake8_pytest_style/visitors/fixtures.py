import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    ExtraneousScopeFunction,
    FixtureParamWithoutValue,
    FixturePositionalArgs,
    IncorrectFixtureNameUnderscore,
    IncorrectFixtureParenthesesStyle,
    MissingFixtureNameUnderscore,
)
from flake8_pytest_style.utils import (
    AnyFunctionDef,
    get_fixture_decorator,
    is_test_function,
)


class FixturesVisitor(Visitor[Config]):
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
            self._check_fixture_decorator(fixture_decorator, node)
            self._check_fixture_returns(node)

        if is_test_function(node):
            self._check_test_function_args(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815
