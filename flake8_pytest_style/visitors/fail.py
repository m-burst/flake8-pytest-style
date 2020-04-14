import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import AssertAlwaysFalse, FailWithoutMessage
from flake8_pytest_style.utils import (
    get_simple_call_args,
    is_empty_string,
    is_fail_call,
    is_falsy_constant,
)


class FailVisitor(Visitor[Config]):
    def _check_fail_call(self, node: ast.Call) -> None:
        """Checks for PT016."""
        args = get_simple_call_args(node)
        msg_argument = args.get_argument('msg', 0)
        if not msg_argument or is_empty_string(msg_argument):
            self.error_from_node(FailWithoutMessage, node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """Checks for PT015."""
        if is_falsy_constant(node.test):
            self.error_from_node(AssertAlwaysFalse, node)

    def visit_Call(self, node: ast.Call) -> None:
        if is_fail_call(node):
            self._check_fail_call(node)
