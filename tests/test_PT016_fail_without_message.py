import pytest
from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import FailWithoutMessage
from flake8_pytest_style.visitors import FailVisitor


def test_ok_arg():
    code = """
        def test_xxx():
            pytest.fail('this is a failure')
    """
    assert_not_error(FailVisitor, code)


def test_ok_kwarg():
    code = """
        def test_xxx():
            pytest.fail(reason='this is a failure')
    """
    assert_not_error(FailVisitor, code)


def test_ok_kwarg_legacy():
    code = """
        def test_xxx():
            pytest.fail(msg='this is a failure')
    """
    assert_not_error(FailVisitor, code)


@pytest.mark.parametrize(
    'args', ['', '""', 'f""', 'reason=""', 'reason=f""', 'msg=""', 'msg=f""']
)
def test_error(args):
    code = f"""
        def test_xxx():
            pytest.fail({args})
    """
    assert_error(FailVisitor, code, FailWithoutMessage)
