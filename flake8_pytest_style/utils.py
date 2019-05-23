import ast
from typing import Union

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
