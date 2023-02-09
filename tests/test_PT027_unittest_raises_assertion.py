from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import UnittestRaisesAssertion
from flake8_pytest_style.visitors import UnittestAssertionVisitor


def test_ok_no_parameters():
    code = """
        import pytest

        def test_xxx():
            with pytest.raises(ValueError):
                raise ValueError()
    """
    assert_not_error(UnittestAssertionVisitor, code)


def test_error():
    code = """
        import pytest

        def test_xxx():
            with self.assertRaises(ValueError):
                raise ValueError()
    """
    assert_error(
        UnittestAssertionVisitor,
        code,
        UnittestRaisesAssertion,
        assertion="assertRaises",
    )
