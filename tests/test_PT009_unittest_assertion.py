from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import UnittestAssertion
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_no_parameters():
    code = """
        import pytest

        def test_xxx():
            assert 1 == 1
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error():
    code = """
        import pytest

        def test_xxx():
            self.assertEqual(1, 1)
    """
    assert_error(PytestStyleVisitor, code, UnittestAssertion, assertion='assertEqual')
