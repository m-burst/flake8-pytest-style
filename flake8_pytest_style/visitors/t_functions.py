import ast
from typing import Optional

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import (
    FixtureParamWithoutValue,
    TFunctionArgumentWithDefault,
)
from flake8_pytest_style.utils import (
    AnyFunctionDef,
    get_qualname,
    get_simple_call_args,
    is_test_function,
)

_PATCH_NAMES = ("patch", "mock.patch", "unittest.mock.patch")
_PATCH_OBJECT_NAMES = tuple(f"{name}.object" for name in _PATCH_NAMES)
_DEFAULT_NAMES = ("DEFAULT", "mock.DEFAULT", "unittest.mock.DEFAULT")


def _injects_mock(decorator: ast.expr) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    name = get_qualname(decorator.func)
    if name not in _PATCH_NAMES + _PATCH_OBJECT_NAMES:
        return False
    # Expanded arguments can supply `new`, so their effect is unknown.
    if any(isinstance(arg, ast.Starred) for arg in decorator.args) or any(
        keyword.arg is None for keyword in decorator.keywords
    ):
        return False
    args = get_simple_call_args(decorator)
    new_arg_number = 1
    if name in _PATCH_OBJECT_NAMES:
        new_arg_number = 2
    new = args.get_argument("new", new_arg_number)
    return new is None or get_qualname(new) in _DEFAULT_NAMES


# This should be named `TestFunctionsVisitor` (and the module `test_functions`),
# but this way it is easier to avoid confusion with the `Test` prefix in pytest.
class TFunctionsVisitor(Visitor[Config]):
    def __init__(self, config: Optional[Config] = None) -> None:
        super().__init__(config=config)
        self._class: Optional[ast.ClassDef] = None

    def _get_mock_args(self, node: AnyFunctionDef) -> list[ast.arg]:
        decorators = node.decorator_list
        if self._class is not None:
            decorators = decorators + self._class.decorator_list
        count = sum(_injects_mock(decorator) for decorator in decorators)
        is_bound_method = self._class is not None and not any(
            get_qualname(decorator) == "staticmethod"
            for decorator in node.decorator_list
        )
        offset = int(is_bound_method)
        positional = node.args.posonlyargs + node.args.args
        return positional[offset : offset + count]  # noqa: E203

    def _check_test_function_args(self, node: AnyFunctionDef) -> None:
        """Checks for PT019, P028."""
        # intentionally not looking at posonlyargs because pytest passes everything
        # as kwargs, so declaring fixture args as positional-only will fail anyway
        mock_args = self._get_mock_args(node)
        for arg in node.args.args + node.args.kwonlyargs:
            if arg.arg.startswith("_") and arg not in mock_args:
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

        # Class decorators apply to methods, not functions nested inside them.
        current_class, self._class = self._class, None
        self.generic_visit(node)
        self._class = current_class

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        current_class, self._class = self._class, node
        self.generic_visit(node)
        self._class = current_class
