import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import UnittestAssertion

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
