import ast
from typing import Optional

from flake8_plugin_utils import Visitor

from ..config import Config
from ..errors import ParametrizeNamesWrongType, ParametrizeValuesWrongType
from ..utils import extract_parametrize_call_args, is_parametrize_call


class ParametrizeVisitor(Visitor[Config]):
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

    def visit_Call(self, node: ast.Call) -> None:
        if is_parametrize_call(node):
            self._check_parametrize_call(node)
