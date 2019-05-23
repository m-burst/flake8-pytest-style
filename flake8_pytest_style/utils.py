import ast
from typing import Union, NamedTuple, Optional

AnyFunctionDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]


def _check_qualname(node: ast.Attribute, qualname: str) -> bool:
    parts = qualname.split('.')

    while len(parts) > 1:
        part = parts.pop()
        if not isinstance(node, ast.Attribute) or node.attr != part:
            return False

        node = node.value

    return isinstance(node, ast.Name) and node.id == parts[0]


def is_parametrize_call(node: ast.Call) -> bool:
    return _check_qualname(node.func, 'pytest.mark.parametrize')


class ParametrizeArgs(NamedTuple):
    names: ast.AST
    values: Optional[ast.AST]
    ids: Optional[ast.AST]


def extract_parametrize_call_args(node: ast.Call) -> Optional[ParametrizeArgs]:
    # list of leading non-starred args
    args = []
    for arg in node.args:
        if isinstance(arg, ast.Starred):
            break
        args.append(arg)

    # dict of keyword args
    keywords = {}
    for keyword in node.keywords:
        if keyword.arg is not None:
            keywords[keyword.arg] = keyword.value

    names_arg = keywords.get('argnames')
    if names_arg is None:
        if len(args) >= 1:
            names_arg = args[0]
        else:
            return None

    values_arg = keywords.get('argvalues')
    if values_arg is None and len(args) >= 2:
        values_arg = args[1]

    ids_arg = keywords.get('ids')

    return ParametrizeArgs(names_arg, values_arg, ids_arg)


def is_test_function(node: AnyFunctionDef) -> bool:
    return node.name.startswith('test_')


def is_pytest_fixture(node: ast.AST) -> bool:
    return isinstance(node, ast.Attribute) and _check_qualname(node, 'pytest.fixture')


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
            and is_pytest_fixture(decorator.func)
        ):
            return decorator
        if isinstance(decorator, ast.Attribute) and is_pytest_fixture(decorator):
            return decorator

    return None
