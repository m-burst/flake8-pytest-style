import ast
from typing import Optional, Union

from flake8_plugin_utils import Visitor

from .errors import (
    ExtraneousScopeFunction,
    FixturePositionalArgs,
    IncorrectFixtureNameUnderscore,
    MissingFixtureNameUnderscore,
    MissingFixtureParentheses,
    ParametrizeNamesWrongType,
    ParametrizeValuesWrongType,
    PatchWithLambda,
)
from .utils import (
    AnyFunctionDef,
    extract_parametrize_call_args,
    get_fixture_decorator,
    get_qualname,
    get_simple_call_args,
    is_parametrize_call,
)

_PATCH_NAMES = ('mocker.patch', 'mock.patch', 'unittest.mock.patch', 'patch')
_PATCH_OBJECT_NAMES = tuple(f'{name}.object' for name in _PATCH_NAMES)


class PytestStyleVisitor(Visitor):
    def _check_fixture_decorator(
        self,
        fixture_decorator: Union[ast.Call, ast.Attribute],
        fixture_func: AnyFunctionDef,
    ) -> None:
        """Checks for PT001, PT002, PT003."""
        if not isinstance(fixture_decorator, ast.Call):
            self.error_from_node(MissingFixtureParentheses, fixture_decorator)
            return

        if fixture_decorator.args:
            self.error_from_node(
                FixturePositionalArgs, fixture_decorator, name=fixture_func.name
            )

        for keyword in fixture_decorator.keywords:
            if (
                keyword.arg == 'scope'
                and isinstance(keyword.value, ast.Str)
                and keyword.value.s == 'function'
            ):
                self.error_from_node(
                    ExtraneousScopeFunction, fixture_decorator, name=fixture_func.name
                )

    def _check_fixture_returns(self, node: AnyFunctionDef) -> None:
        """Checks for PT004, PT005."""
        has_return_with_value = False
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                has_return_with_value = True
                break

        if has_return_with_value and node.name.startswith('_'):
            self.error_from_node(IncorrectFixtureNameUnderscore, node, name=node.name)
        elif not has_return_with_value and not node.name.startswith('_'):
            self.error_from_node(MissingFixtureNameUnderscore, node, name=node.name)

    def _check_parametrize_names(
        self, node: ast.Call, names: ast.AST
    ) -> Optional[bool]:
        """
        Handles names in parametrize, checks for PT006.

        Returns a flag indicating whether parametrize has multiple names,
        or None if we can't tell.
        """

        multiple_names: Optional[bool] = None
        if isinstance(names, ast.Str):
            if ',' in names.s:
                self.error_from_node(
                    ParametrizeNamesWrongType, node, expected_type='tuple'
                )
                multiple_names = True
            else:
                multiple_names = False
        elif isinstance(names, (ast.List, ast.Tuple)):
            multiple_names = len(names.elts) > 1
            if not multiple_names:
                self.error_from_node(
                    ParametrizeNamesWrongType, node, expected_type='string'
                )
            elif not isinstance(names, ast.Tuple):
                self.error_from_node(
                    ParametrizeNamesWrongType, node, expected_type='tuple'
                )
        return multiple_names

    def _check_parametrize_values(
        self, node: ast.Call, values: Optional[ast.AST], multiple_names: Optional[bool]
    ) -> None:
        """Checks for PT007."""
        if isinstance(values, ast.Tuple):
            if multiple_names:
                self.error_from_node(
                    ParametrizeValuesWrongType, node, expected_type='list of tuples'
                )
            else:
                self.error_from_node(
                    ParametrizeValuesWrongType, node, expected_type='list'
                )
        elif isinstance(values, ast.List) and multiple_names:
            for element in values.elts:
                if isinstance(element, ast.List):
                    self.error_from_node(
                        ParametrizeValuesWrongType, node, expected_type='list of tuples'
                    )
                    break

    def _check_parametrize_call(self, node: ast.Call) -> None:
        """Checks for all violations regarding `pytest.mark.parametrize` calls."""
        args = extract_parametrize_call_args(node)
        if not args:
            return

        multiple_names = self._check_parametrize_names(node, args.names)

        self._check_parametrize_values(node, args.values, multiple_names)

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

        lambda_argnames = {
            arg.arg for arg in new_arg.args.args + new_arg.args.kwonlyargs
        }
        if new_arg.args.vararg:
            lambda_argnames.add(new_arg.args.vararg.arg)
        if new_arg.args.kwarg:
            lambda_argnames.add(new_arg.args.kwarg.arg)

        for child_node in ast.walk(new_arg.body):
            if isinstance(child_node, ast.Name) and child_node.id in lambda_argnames:
                break
        else:
            self.error_from_node(PatchWithLambda, node)

    def visit_FunctionDef(self, node: AnyFunctionDef) -> None:  # noqa: N802
        fixture_decorator = get_fixture_decorator(node)
        if fixture_decorator:
            self._check_fixture_decorator(fixture_decorator, node)
            self._check_fixture_returns(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        if is_parametrize_call(node):
            self._check_parametrize_call(node)

        if get_qualname(node.func) in _PATCH_NAMES:
            # attributes are (target, new, ...)
            self._check_patch_call(node, 1)

        if get_qualname(node.func) in _PATCH_OBJECT_NAMES:
            # attributes are (target, attribute, new, ...)
            self._check_patch_call(node, 2)
