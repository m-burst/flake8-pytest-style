from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    FixtureParamWithoutValue,
    TFunctionArgumentWithDefault,
)
from flake8_pytest_style.utils import AnyFunctionDef, is_test_function


# This should be named `TestFunctionsVisitor` (and the module `test_functions`),
# but this way it is easier to avoid confusion with the `Test` prefix in pytest.
class TFunctionsVisitor(Visitor[Config]):
    def _check_test_function_args(self, node: AnyFunctionDef) -> None:
        """Checks for PT019, P028."""
        # intentionally not looking at posonlyargs because pytest passes everything
        # as kwargs, so declaring fixture args as positional-only will fail anyway
        for arg in node.args.args + node.args.kwonlyargs:
            if arg.arg.startswith('_'):
                # The error is raised at the position of `node` (function call),
                # not `arg`, to preserve backwards compatibility.
                self.error_from_node(FixtureParamWithoutValue, node, name=arg.arg)

        if node.args.defaults:
            pos_args = node.args.posonlyargs + node.args.args
            pos_args_with_defaults = pos_args[-len(node.args.defaults) :]  # noqa: E203
            for arg in pos_args_with_defaults:
                self.error_from_node(
                    TFunctionArgumentWithDefault, arg, name=node.name, arg=arg.arg
                )

        for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
            if default is not None:
                self.error_from_node(
                    TFunctionArgumentWithDefault, arg, name=node.name, arg=arg.arg
                )

    def visit_FunctionDef(self, node: AnyFunctionDef) -> None:
        if is_test_function(node):
            self._check_test_function_args(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815
