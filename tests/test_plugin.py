import importlib
import inspect
import pkgutil
from collections import Counter
from types import ModuleType
from typing import List, Set, Type, TypeVar

from flake8_pytest_style.plugin import PytestStylePlugin

T = TypeVar('T')


def _collect_subclasses(modules: List[ModuleType], base_class: Type[T]) -> Set[Type[T]]:
    result = set()
    for module in modules:
        for _, member in inspect.getmembers(module):
            if (
                inspect.isclass(member)
                and issubclass(member, base_class)
                and member is not base_class
            ):
                result.add(member)
    return result


def test_plugin_has_all_visitors():
    from flake8_plugin_utils import Visitor
    from flake8_pytest_style import visitors as visitors_package

    visitor_module_infos = pkgutil.iter_modules(
        visitors_package.__path__  # type: ignore
    )
    visitor_modules = [
        importlib.import_module(
            f'{visitors_package.__name__}.{visitor_module_info.name}'
        )
        for visitor_module_info in visitor_module_infos
    ]
    visitor_classes = _collect_subclasses(visitor_modules, Visitor)

    assert set(PytestStylePlugin.visitors) == visitor_classes


def test_all_error_codes_are_different():
    from flake8_plugin_utils import Error
    from flake8_pytest_style import errors

    error_classes = _collect_subclasses([errors], Error)
    count_by_code = Counter(error_class.code for error_class in error_classes)
    duplicate_error_codes = [code for code, count in count_by_code.items() if count > 1]
    assert not duplicate_error_codes
