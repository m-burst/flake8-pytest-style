import ast
from typing import Union

from flake8_pytest_style.errors import IncorrectFixtureNameUnderscore, \
    MissingFixtureNameUnderscore, ParametrizeNamesWrongType
from flake8_pytest_style.utils import is_parametrize_call, extract_parametrize_call_args
from ._vendor.flake8_plugin_utils import Visitor
from .errors import (
    ExtraneousScopeFunction,
    FixturePositionalArgs,
    MissingFixtureParentheses,
)
from .utils import AnyFunctionDef, get_fixture_decorator


class PytestStyleVisitor(Visitor):
    def _check_fixture_decorator(
        self,
        fixture_decorator: Union[ast.Call, ast.Attribute],
        fixture_func: AnyFunctionDef,
    ):
        """Checks for PT001, PT002, PT003."""
        if not isinstance(fixture_decorator, ast.Call):
            self.error_from_node(MissingFixtureParentheses, fixture_decorator)
            return

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

    def _check_fixture_returns(self, node: AnyFunctionDef):
        """Checks for PT004, PT005."""
        has_return_with_value = False
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                has_return_with_value = True
                break

        if has_return_with_value and node.name.startswith('_'):
            self.error_from_node(IncorrectFixtureNameUnderscore, node, name=node.name)
        elif not has_return_with_value and not node.name.startswith('_'):
            self.error_from_node(MissingFixtureNameUnderscore, node, name=node.name)

    def _check_parametrize_call(self, node: ast.Call):
        args = extract_parametrize_call_args(node)
        if not args:
            return

        if isinstance(args.names, ast.Str):
            if ',' in args.names.s:
                self.error_from_node(
                    ParametrizeNamesWrongType,
                    node,
                    expected_type='tuple',
                )
                arg_count = len(args.names.s.split(','))
            else:
                arg_count = 1
        elif isinstance(args.names, (ast.List, ast.Tuple)):
            arg_count = len(args.names.elts)
            if arg_count == 1:
                self.error_from_node(
                    ParametrizeNamesWrongType,
                    node,
                    expected_type='string',
                )
            elif not isinstance(args.names, ast.Tuple):
                self.error_from_node(
                    ParametrizeNamesWrongType,
                    node,
                    expected_type='tuple',
                )

    def visit_FunctionDef(self, node: AnyFunctionDef):
        fixture_decorator = get_fixture_decorator(node)
        if fixture_decorator:
            self._check_fixture_decorator(fixture_decorator, node)
            self._check_fixture_returns(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call):
        if is_parametrize_call(node):
            self._check_parametrize_call(node)
