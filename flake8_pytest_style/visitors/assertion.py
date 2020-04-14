import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import CompositeAssertion, UnittestAssertion

_UNITTEST_ASSERT_NAMES = (
    'assertAlmostEqual',
    'assertAlmostEquals',
    'assertDictEqual',
    'assertEqual',
    'assertEquals',
    'assertFalse',
    'assertGreater',
    'assertGreaterEqual',
    'assertIn',
    'assertIs',
    'assertIsInstance',
    'assertIsNone',
    'assertIsNot',
    'assertIsNotNone',
    'assertItemsEqual',
    'assertLess',
    'assertLessEqual',
    'assertMultiLineEqual',
    'assertNotAlmostEqual',
    'assertNotAlmostEquals',
    'assertNotContains',
    'assertNotEqual',
    'assertNotEquals',
    'assertNotIn',
    'assertNotIsInstance',
    'assertNotRegexpMatches',
    'assertRaises',
    'assertRaisesMessage',
    'assertRaisesRegexp',
    'assertRegexpMatches',
    'assertSetEqual',
    'assertTrue',
    'assert_',
)


class UnittestAssertionVisitor(Visitor[Config]):
    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in _UNITTEST_ASSERT_NAMES
        ):
            self.error_from_node(UnittestAssertion, node, assertion=node.func.attr)


class AssertionVisitor(Visitor[Config]):
    def _is_composite_condition(self, expr: ast.AST) -> bool:
        # e.g. `a and b`
        if isinstance(expr, ast.BoolOp) and isinstance(expr.op, ast.And):
            return True

        # e.g. `not (a or b)`
        if (
            isinstance(expr, ast.UnaryOp)
            and isinstance(expr.op, ast.Not)
            and isinstance(expr.operand, ast.BoolOp)
            and isinstance(expr.operand.op, ast.Or)
        ):
            return True

        return False

    def visit_Assert(self, node: ast.Assert) -> None:
        if self._is_composite_condition(node.test):
            self.error_from_node(CompositeAssertion, node)
