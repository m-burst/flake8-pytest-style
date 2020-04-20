import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import PatchWithLambda
from flake8_pytest_style.utils import (
    get_all_argument_names,
    get_qualname,
    get_simple_call_args,
)

_PATCH_NAMESPACES = (
    'mocker',
    'class_mocker',
    'module_mocker',
    'package_mocker',
    'session_mocker',
    'mock',
    'unittest.mock',
)
_PATCH_NAMES = ('patch',) + tuple(
    f'{namespace}.patch' for namespace in _PATCH_NAMESPACES
)
_PATCH_OBJECT_NAMES = tuple(f'{name}.object' for name in _PATCH_NAMES)


class PatchVisitor(Visitor[Config]):
    def _check_patch_call(self, node: ast.Call, new_arg_number: int) -> None:
        """
        Checks for PT008.

        :param node: patch call node
        :param new_arg_number: number of `new` positional argument of patch func
        """
        args = get_simple_call_args(node)
        if args.get_argument('return_value') is not None:
            return

        new_arg = args.get_argument('new', new_arg_number)
        if not isinstance(new_arg, ast.Lambda):
            return

        lambda_argnames = set(get_all_argument_names(new_arg.args))

        for child_node in ast.walk(new_arg.body):
            if isinstance(child_node, ast.Name) and child_node.id in lambda_argnames:
                break
        else:
            self.error_from_node(PatchWithLambda, node)

    def visit_Call(self, node: ast.Call) -> None:
        if get_qualname(node.func) in _PATCH_NAMES:
            # attributes are (target, new, ...)
            self._check_patch_call(node, 1)

        if get_qualname(node.func) in _PATCH_OBJECT_NAMES:
            # attributes are (target, attribute, new, ...)
            self._check_patch_call(node, 2)
