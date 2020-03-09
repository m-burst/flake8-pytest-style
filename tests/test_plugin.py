import importlib
import inspect
import pkgutil

from flake8_pytest_style.plugin import PytestStylePlugin


def test_plugin_has_all_visitors():
    from flake8_pytest_style import visitors as visitors_package
    from flake8_plugin_utils import Visitor

    visitor_classes = set()
    for visitor_module_info in pkgutil.iter_modules(
        visitors_package.__path__  # type: ignore
    ):
        visitor_module = importlib.import_module(
            f'{visitors_package.__name__}.{visitor_module_info.name}'
        )
        for name, member in inspect.getmembers(visitor_module):
            if (
                inspect.isclass(member)
                and issubclass(member, Visitor)
                and member is not Visitor
            ):
                visitor_classes.add(member)

    assert set(PytestStylePlugin.visitors) == visitor_classes
