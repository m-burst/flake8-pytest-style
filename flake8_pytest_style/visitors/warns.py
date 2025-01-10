import ast

from flake8_plugin_utils import Visitor, is_none

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    WarnsTooBroad,
    WarnsWithMultipleStatements,
    WarnsWithoutException,
)
from flake8_pytest_style.utils import (
    get_qualname,
    get_simple_call_args,
    is_empty_string,
    is_nontrivial_with_statement,
    is_warns_call,
    is_warns_with,
)


class WarnsVisitor(Visitor[Config]):
    def _check_warns_call(self, node: ast.Call) -> None:
        """
        Checks for violations regarding `pytest.warns` call args (PT029 and PT030).
        """
        args = get_simple_call_args(node)
        warning = args.get_argument('expected_warning', position=0)
        if not warning:
            self.error_from_node(WarnsWithoutException, node)
            return

        warning_name = get_qualname(warning)
        if warning_name not in self.config.warns_require_match_for:
            return
        match = args.get_argument('match')
        if match is None or is_none(match) or is_empty_string(match):
            self.error_from_node(WarnsTooBroad, node, warning=warning_name)

    def _check_warns_with(self, node: ast.With) -> None:
        """Checks for PT031."""
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
            self.error_from_node(WarnsWithMultipleStatements, node)

    def visit_Call(self, node: ast.Call) -> None:
        if is_warns_call(node):
            self._check_warns_call(node)

    def visit_With(self, node: ast.With) -> None:
        if is_warns_with(node):
            self._check_warns_with(node)

        self.generic_visit(node)
