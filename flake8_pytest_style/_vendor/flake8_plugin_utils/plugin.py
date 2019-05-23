import ast
import re
from typing import Any, Iterable, List, Tuple, Type

FLAKE8_ERROR = Tuple[int, int, str, 'Plugin']
NOQA_REGEXP = re.compile(r'#.*noqa\s*($|[^:\s])', re.I)
NOQA_ERROR_CODE_REGEXP = re.compile(r'#.*noqa\s*:\s*(\w+)', re.I)


class Error:
    code: str
    message: str
    lineno: int
    col_offset: int

    def __init__(self, lineno: int, col_offset: int, **kwargs: Any) -> None:
        self.lineno = lineno
        self.col_offset = col_offset
        self.message = self.formatted_message(**kwargs)

    @classmethod
    def formatted_message(cls, **kwargs: Any) -> str:
        return cls.message.format(**kwargs)


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Error] = []

    def error_from_node(
        self, error: Type[Error], node: ast.AST, **kwargs: Any
    ) -> None:
        self.errors.append(error(node.lineno, node.col_offset, **kwargs))


class Plugin:
    name: str
    version: str
    visitors: List[Type[Visitor]]

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self._tree: ast.AST = tree
        self._filename: str = filename
        self._lines: List[str] = []

    def run(self) -> Iterable[FLAKE8_ERROR]:
        if not self._tree or not self._lines:
            self._load_file()

        for visitor in self.visitors:
            _visitor = visitor()
            _visitor.visit(self._tree)

            for error in _visitor.errors:
                line = self._lines[error.lineno - 1]
                if not check_noqa(line, error.code):
                    yield self._error(error)

    def _load_file(self) -> None:
        with open(self._filename) as f:
            self._lines = f.readlines()
        self._tree = ast.parse(''.join(self._lines))

    def _error(self, error: Error) -> FLAKE8_ERROR:
        return (
            error.lineno,
            error.col_offset,
            f'{error.code} {error.message}',
            self,
        )

    @classmethod
    def add_visitor(cls, visitor_cls: Type[Visitor]) -> Type[Visitor]:
        cls.visitors.append(visitor_cls)
        return visitor_cls


def check_noqa(line: str, code: str) -> bool:
    if NOQA_REGEXP.search(line):
        return True

    match = NOQA_ERROR_CODE_REGEXP.search(line)
    if match:
        return match.groups()[0].lower() == code.lower()

    return False
