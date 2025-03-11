import ast
from typing import Any

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import CallableRaisesWarnsDeprecatedcall
from flake8_pytest_style.utils import (
    is_deprecatedcall_call,
    is_raises_call,
    is_warns_call,
)


class CallableRaisesWarnsDeprecatedcallVisitor(Visitor[Config]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._in_with: bool = False

    def visit_With(self, node: ast.With) -> None:
        old_in_with = self._in_with
        self._in_with = True
        for item in node.items:
            self.visit(item)
        self._in_with = old_in_with
        for body in node.body:
            self.visit(body)

    def visit_Call(self, node: ast.Call) -> None:
        if not self._in_with:
            if is_raises_call(node):
                self.error_from_node(
                    CallableRaisesWarnsDeprecatedcall, node, name='raises'
                )
            if is_warns_call(node):
                self.error_from_node(
                    CallableRaisesWarnsDeprecatedcall, node, name='warns'
                )
            if is_deprecatedcall_call(node):
                self.error_from_node(
                    CallableRaisesWarnsDeprecatedcall, node, name='deprecated_call'
                )
