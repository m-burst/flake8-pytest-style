import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import IncorrectPytestImport
from flake8_pytest_style.visitors.imports import ImportsVisitor


@pytest.mark.parametrize(
    "code",
    [
        "import pytest",
        "import pytest as pytest",
        "from notpytest import fixture",
        "from . import fixture",
        "from .pytest import fixture",
    ],
)
def test_ok(code):
    assert_not_error(ImportsVisitor, code)


@pytest.mark.parametrize(
    "code",
    [
        "import pytest as other_name",
        "from pytest import fixture",
        "from pytest import fixture as other_name",
    ],
)
def test_error(code):
    assert_error(ImportsVisitor, code, IncorrectPytestImport)
