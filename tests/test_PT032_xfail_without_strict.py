import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import XfailWithoutStrict
from flake8_pytest_style.visitors import MarksVisitor


def test_ok_with_strict_true():
    code = """
import pytest

@pytest.mark.xfail(strict=True)
def test_something():
    pass
"""
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_strict_false():
    code = """
import pytest

@pytest.mark.xfail(strict=False)
def test_something():
    pass
"""
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_strict_and_reason():
    code = """
import pytest

@pytest.mark.xfail(reason="broken", strict=True)
def test_something():
    pass
"""
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_error_without_strict_no_parens():
    code = """
import pytest

@pytest.mark.xfail
def test_something():
    pass
"""
    assert_error(MarksVisitor, code, XfailWithoutStrict, config=DEFAULT_CONFIG)


def test_error_without_strict_with_reason():
    code = """
import pytest

@pytest.mark.xfail(reason="broken")
def test_something():
    pass
"""
    assert_error(MarksVisitor, code, XfailWithoutStrict, config=DEFAULT_CONFIG)
