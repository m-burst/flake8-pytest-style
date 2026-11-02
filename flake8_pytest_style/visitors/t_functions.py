import ast
from typing import Set

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    FixtureParamWithoutValue,
    TFunctionArgumentWithDefault,
)
from flake8_pytest_style.utils import (
    AnyFunctionDef,
    extract_parametrize_call_args,
    is_parametrize_call,
    is_test_function,
)


# This should be named `TestFunctionsVisitor` (and the module `test_functions`),
# but this way it is easier to avoid confusion with the `Test` prefix in pytest.
class TFunctionsVisitor(Visitor[Config]):
    def _names_from_parametrize_argnames(self, names_node: ast.AST) -> Set[str]:
        """Return statically identifiable names from a parametrize argnames node."""
        if isinstance(names_node, ast.Constant) and isinstance(names_node.value, str):
            return {
                name.strip() for name in names_node.value.split(",") if name.strip()
            }
        if isinstance(names_node, (ast.List, ast.Tuple)):
            return {
                elt.value
                for elt in names_node.elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            }
        return set()

    def _get_parametrize_arg_names(self, node: AnyFunctionDef) -> Set[str]:
        """Collect parametrize argument names from decorators on the function."""
        names: Set[str] = set()
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not is_parametrize_call(
                decorator
            ):
                continue
            args = extract_parametrize_call_args(decorator)
            if args is None:
                continue
            names.update(self._names_from_parametrize_argnames(args.names))
        return names

    def _check_test_function_args(self, node: AnyFunctionDef) -> None:
        """Checks for PT019, P028."""
        # intentionally not looking at posonlyargs because pytest passes everything
        # as kwargs, so declaring fixture args as positional-only will fail anyway
        parametrized_names = self._get_parametrize_arg_names(node)
        for arg in node.args.args + node.args.kwonlyargs:
            if arg.arg.startswith("_") and arg.arg not in parametrized_names:
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
