import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    CompositeAssertion,
    UnittestAssertion,
    UnittestRaisesAssertion,
)

_UNITTEST_ASSERT_NAMES = (
    # taken from dir(unittest.TestCase) under Python 3.11
    'assertAlmostEqual',
    'assertAlmostEquals',
    'assertCountEqual',
    'assertDictContainsSubset',
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
    'assertLess',
    'assertLessEqual',
    'assertListEqual',
    'assertLogs',
    'assertMultiLineEqual',
    'assertNoLogs',
    'assertNotAlmostEqual',
    'assertNotAlmostEquals',
    'assertNotEqual',
    'assertNotEquals',
    'assertNotIn',
    'assertNotIsInstance',
    'assertNotRegex',
    'assertNotRegexpMatches',
    'assertRegex',
    'assertRegexpMatches',
    'assertSequenceEqual',
    'assertSetEqual',
    'assertTrue',
    'assertTupleEqual',
    'assertWarns',
    'assertWarnsRegex',
    'assert_',
    'failIf',
    'failIfAlmostEqual',
    'failIfEqual',
    'failUnless',
    'failUnlessAlmostEqual',
    'failUnlessEqual',
    # below is from Django's SimpleTestCase, leaked here when porting flake8-pytest
    # TODO(m_burst) disallow Django's SimpleTestCase/TransactionTestCase assertions
    #  where feasible (#220)
    'assertNotContains',
)

_UNITTEST_ASSERT_RAISES_NAMES = (
    # taken from dir(unittest.TestCase) under Python 3.11
    'assertRaises',
    'assertRaisesRegex',
    'assertRaisesRegexp',
    'failUnlessRaises',
    # below is from Django's SimpleTestCase, leaked here when porting flake8-pytest
    'assertRaisesMessage',
)


class UnittestAssertionVisitor(Visitor[Config]):
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in _UNITTEST_ASSERT_NAMES:
                self.error_from_node(UnittestAssertion, node, assertion=node.func.attr)
            elif node.func.attr in _UNITTEST_ASSERT_RAISES_NAMES:
                self.error_from_node(
                    UnittestRaisesAssertion, node, assertion=node.func.attr
                )


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
