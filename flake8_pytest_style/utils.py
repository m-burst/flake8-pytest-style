import ast
from typing import Dict, NamedTuple, Optional, Tuple, Union

AnyFunctionDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]


def get_qualname(node: ast.AST) -> Optional[str]:
    """
    If node represents a chain of attribute accesses, return is qualified name.
    """
    parts = []
    while True:
        if isinstance(node, ast.Name):
            parts.append(node.id)
            break
        if isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        else:
            return None
    return '.'.join(reversed(parts))


class SimpleCallArgs(NamedTuple):
    args: Tuple[ast.AST, ...]
    kwargs: Dict[str, ast.AST]

    def get_argument(
        self, name: str, position: Optional[int] = None
    ) -> Optional[ast.AST]:
        """Get argument by name in kwargs or position in args."""
        kwarg = self.kwargs.get(name)
        if kwarg is not None:
            return kwarg
        if position is not None and len(self.args) > position:
            return self.args[position]
        return None


def get_simple_call_args(node: ast.Call) -> SimpleCallArgs:
    """
    Get call arguments which are specified explicitly (positional and keyword).
    """

    # list of leading non-starred args
    args = []
    for arg in node.args:
        if isinstance(arg, ast.Starred):
            break
        args.append(arg)

    # dict of keyword args
    keywords: Dict[str, ast.AST] = {}
    for keyword in node.keywords:
        if keyword.arg is not None:
            keywords[keyword.arg] = keyword.value

    return SimpleCallArgs(tuple(args), keywords)


def is_parametrize_call(node: ast.Call) -> bool:
    """Checks if given call is to `pytest.mark.parametrize`."""
    return get_qualname(node.func) == 'pytest.mark.parametrize'


def is_raises_call(node: ast.Call) -> bool:
    """Checks if given call is to `pytest.raises`."""
    return get_qualname(node.func) == 'pytest.raises'


def is_raises_with(node: ast.With) -> bool:
    """Checks that a given `with` statement has a `pytest.raises` context."""
    for item in node.items:
        if isinstance(item.context_expr, ast.Call) and is_raises_call(
            item.context_expr
        ):
            return True
    return False


class ParametrizeArgs(NamedTuple):
    names: ast.AST
    values: Optional[ast.AST]
    ids: Optional[ast.AST]


def extract_parametrize_call_args(node: ast.Call) -> Optional[ParametrizeArgs]:
    """Extracts argnames, argvalues and ids from a parametrize call."""
    args = get_simple_call_args(node)

    names_arg = args.get_argument('argnames', 0)
    if names_arg is None:
        return None

    values_arg = args.get_argument('argvalues', 1)
    ids_arg = args.get_argument('ids')
    return ParametrizeArgs(names_arg, values_arg, ids_arg)


def _is_pytest_fixture(node: ast.AST) -> bool:
    """Checks if node is a `pytest.fixture` attribute access."""
    return get_qualname(node) == 'pytest.fixture'


def get_fixture_decorator(node: AnyFunctionDef) -> Union[ast.Call, ast.Attribute, None]:
    """
    Returns a @pytest.fixture decorator applied to given function definition, if any.

    Return value is either:
    * ast.Call, if decorator is written as @pytest.fixture()
    * ast.Attribute, if decorator is written as @pytest.fixture
    * None, if decorator not found
    """
    for decorator in node.decorator_list:
        if (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and _is_pytest_fixture(decorator.func)
        ):
            return decorator
        if isinstance(decorator, ast.Attribute) and _is_pytest_fixture(decorator):
            return decorator

    return None
