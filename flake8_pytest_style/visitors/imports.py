import ast

from flake8_plugin_utils import Visitor

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import IncorrectPytestImport


def _is_pytest_or_subpackage(imported_name: str) -> bool:
    return imported_name == 'pytest' or imported_name.startswith('pytest.')


class ImportsVisitor(Visitor[Config]):
    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if (
                _is_pytest_or_subpackage(name.name)
                and name.asname
                and name.asname != name.name
            ):
                self.error_from_node(IncorrectPytestImport, node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level != 0 or node.module is None:  # relative import
            return
        if _is_pytest_or_subpackage(node.module):
            self.error_from_node(IncorrectPytestImport, node)
