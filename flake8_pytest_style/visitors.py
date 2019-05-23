import ast
from typing import Union

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
        pass

    def visit_FunctionDef(self, node: AnyFunctionDef):
        fixture_decorator = get_fixture_decorator(node)
        if fixture_decorator:
            self._check_fixture_decorator(fixture_decorator, node)
            self._check_fixture_returns(node)

    visit_AsyncFunctionDef = visit_FunctionDef
