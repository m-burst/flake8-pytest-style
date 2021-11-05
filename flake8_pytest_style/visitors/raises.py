import ast
from typing import List, Optional

from flake8_plugin_utils import Visitor, is_none

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    AssertInExcept,
    RaisesTooBroad,
    RaisesWithMultipleStatements,
    RaisesWithoutException,
)
from flake8_pytest_style.utils import (
    get_qualname,
    get_simple_call_args,
    is_empty_string,
    is_nontrivial_with_statement,
    is_raises_call,
    is_raises_with,
)


class RaisesVisitor(Visitor[Config]):
    def __init__(self, config: Optional[Config] = None) -> None:
        super().__init__(config=config)
        self._exception_names: List[str] = []
        self._current_assert: Optional[ast.Assert] = None

    def _check_raises_call(self, node: ast.Call) -> None:
        """
        Checks for violations regarding `pytest.raises` call args (PT010 and PT011).
        """
        args = get_simple_call_args(node)
        exception = args.get_argument('expected_exception', position=0)
        if not exception:
            self.error_from_node(RaisesWithoutException, node)
            return

        exception_name = get_qualname(exception)
        if exception_name not in self.config.raises_require_match_for:
            return
        match = args.get_argument('match')
        if match is None or is_none(match) or is_empty_string(match):
            self.error_from_node(RaisesTooBroad, node, exception=exception_name)

    def _check_raises_with(self, node: ast.With) -> None:
        """Checks for PT012."""
        body = node.body

        is_complex_body = False
        if len(body) != 1:
            is_complex_body = True
        elif isinstance(
            body[0],
            (
                ast.If,
                ast.For,
                ast.AsyncFor,
                ast.While,
                ast.Try,
            ),
        ):
            is_complex_body = True
        elif is_nontrivial_with_statement(body[0]):
            is_complex_body = True

        if is_complex_body:
            self.error_from_node(RaisesWithMultipleStatements, node)

    def visit_Call(self, node: ast.Call) -> None:
        if is_raises_call(node):
            self._check_raises_call(node)

    def visit_With(self, node: ast.With) -> None:
        if is_raises_with(node):
            self._check_raises_with(node)

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.name:
            self._exception_names.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            if node.name:
                self._exception_names.pop()

    def visit_Assert(self, node: ast.Assert) -> None:
        self._current_assert = node
        try:
            self.visit(node.test)
        finally:
            self._current_assert = None

        if node.msg:
            self.visit(node.msg)

    def visit_Name(self, node: ast.Name) -> None:
        if self._current_assert:
            if node.id in self._exception_names:
                self.error_from_node(AssertInExcept, self._current_assert, name=node.id)
