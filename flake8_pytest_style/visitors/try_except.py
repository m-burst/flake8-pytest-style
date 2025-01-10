import ast
from typing import List, Optional

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import AssertInExcept


class TryExceptVisitor(Visitor[Config]):
    def __init__(self, config: Optional[Config] = None) -> None:
        super().__init__(config=config)
        self._exception_names: List[str] = []
        self._current_assert: Optional[ast.Assert] = None

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
