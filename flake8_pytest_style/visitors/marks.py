import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import IncorrectMarkParenthesesStyle
from flake8_pytest_style.utils import (
    AnyDecoratorTarget,
    get_mark_decorators,
    get_mark_name,
)


class MarksVisitor(Visitor[Config]):
    def _check_mark_decorator(
        self, mark_decorator: Union[ast.Call, ast.Attribute]
    ) -> None:
        """Checks for PT023."""

        if not isinstance(mark_decorator, ast.Call):
            if self.config.mark_parentheses:
                self.error_from_node(
                    IncorrectMarkParenthesesStyle,
                    mark_decorator,
                    mark_name=get_mark_name(mark_decorator),
                    expected_parens='()',
                    actual_parens='',
                )
            return

        if (
            not self.config.mark_parentheses
            and not mark_decorator.args
            and not mark_decorator.keywords
        ):
            self.error_from_node(
                IncorrectMarkParenthesesStyle,
                mark_decorator,
                mark_name=get_mark_name(mark_decorator.func),
                expected_parens='',
                actual_parens='()',
            )

    def visit_FunctionDef(self, node: AnyDecoratorTarget) -> None:
        mark_decorators = get_mark_decorators(node)
        for mark_decorator in mark_decorators:
            self._check_mark_decorator(mark_decorator)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815
    visit_ClassDef = visit_FunctionDef  # noqa: N815
