import ast
from textwrap import dedent
from typing import Any, Optional, Type

from flake8_plugin_utils import Visitor
from flake8_plugin_utils.plugin import Error, TConfig

from flake8_pytest_style.config import Config
from flake8_pytest_style.errors import NoBareRaises
from flake8_pytest_style.visitors import PytestStyleVisitor

CONFIG = Config(no_bare_raises_exceptions=['ValueError'])


def test_ok():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ValueError, match="Can't divide by 0"):
                raise ValueError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=CONFIG)


def test_ok_different_error_from_config():
    code = """
        import pytest

        def test_something():
            with pytest.raises(ZeroDivisionError):
                raise ZeroDivisionError("Can't divide by 0")
    """
    assert_not_error(PytestStyleVisitor, code, config=CONFIG)


def test_error_no_argument_given():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises, config=CONFIG)


def test_error_match_is_none():
    code = f"""
        import pytest

        def test_something():
            with pytest.raises(ValueError, match=None):
                raise ValueError("Can't divide 1 by 0")
    """
    assert_error(PytestStyleVisitor, code, NoBareRaises, config=CONFIG)


def _error_from_src(
    visitor_cls: Type[Visitor[TConfig]], src: str, config: Optional[TConfig] = None,
) -> Optional[Error]:
    visitor = visitor_cls(config=config)
    tree = ast.parse(dedent(src))
    visitor.visit(tree)
    if not visitor.errors:
        return None
    assert len(visitor.errors) == 1
    return visitor.errors[0]


def assert_error(
    visitor_cls: Type[Visitor[TConfig]],
    src: str,
    expected: Type[Error],
    config: Optional[TConfig] = None,
    **kwargs: Any,
) -> None:
    err = _error_from_src(visitor_cls, src, config=config)
    assert err, f'Error "{expected.message}" not found in\n{src}'
    assert isinstance(err, expected)

    expected_message = expected.formatted_message(**kwargs)
    assert (
        expected_message == err.message
    ), f'Expected error with message "{expected_message}", got "{err.message}"'


def assert_not_error(
    visitor_cls: Type[Visitor[Any]], src: str, config: Optional[TConfig] = None
) -> None:
    err = _error_from_src(visitor_cls, src, config=config)
    assert not err, f'Error "{err.message}" found in\n{src}'  # type: ignore
