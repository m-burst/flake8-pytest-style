import ast
from typing import Optional

from flake8_plugin_utils import Visitor

from ..config import (
    Config,
    ParametrizeNamesType,
    ParametrizeValuesRowType,
    ParametrizeValuesType,
)
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
        found_type: Optional[ParametrizeNamesType] = None
        if isinstance(names, ast.Str):
            if ',' in names.s:
                found_type = ParametrizeNamesType.CSV
                multiple_names = True
            else:
                multiple_names = False
        elif isinstance(names, (ast.List, ast.Tuple)):
            multiple_names = len(names.elts) > 1
            if not multiple_names:
                self.error_from_node(
                    ParametrizeNamesWrongType, node, expected_type='string'
                )
            elif isinstance(names, ast.Tuple):
                found_type = ParametrizeNamesType.TUPLE
            else:
                found_type = ParametrizeNamesType.LIST
        if multiple_names and found_type != self.config.parametrize_names_type:
            self.error_from_node(
                ParametrizeNamesWrongType,
                node,
                expected_type=self.config.parametrize_names_type.value,
            )
        return multiple_names

    def _get_expected_values_type_str(self, multiple_names: Optional[bool]) -> str:
        if multiple_names:
            return (
                f'{self.config.parametrize_values_type.value}'
                f' of {self.config.parametrize_values_row_type.value}s'
            )
        return self.config.parametrize_values_type.value

    def _check_parametrize_values(
        self, node: ast.Call, values: Optional[ast.AST], multiple_names: Optional[bool]
    ) -> None:
        """Checks for PT007."""
        expected_type_str = self._get_expected_values_type_str(multiple_names)

        if isinstance(values, ast.List):
            top_level_type = ParametrizeValuesType.LIST
        elif isinstance(values, ast.Tuple):
            top_level_type = ParametrizeValuesType.TUPLE
        else:
            return

        if top_level_type != self.config.parametrize_values_type:
            self.error_from_node(
                ParametrizeValuesWrongType, node, expected_type=expected_type_str
            )
            return

        if multiple_names:
            for element in values.elts:
                found_row_type: Optional[ParametrizeValuesRowType] = None
                if isinstance(element, ast.List):
                    found_row_type = ParametrizeValuesRowType.LIST
                elif isinstance(element, ast.Tuple):
                    found_row_type = ParametrizeValuesRowType.TUPLE
                if (
                    found_row_type
                    and found_row_type != self.config.parametrize_values_row_type
                ):
                    self.error_from_node(
                        ParametrizeValuesWrongType,
                        node,
                        expected_type=expected_type_str,
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
