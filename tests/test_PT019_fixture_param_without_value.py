from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import FixtureParamWithoutValue
from flake8_pytest_style.visitors import TFunctionsVisitor


def test_ok_good_param_name():
    code = """
        def test_xxx(fixture):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_non_test_function():
    code = """
        def xxx(_param):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_error_arg():
    code = """
        def test_xxx(_fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name='_fixture')


def test_error_kwonly():
    code = """
        def test_xxx(*, _fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name='_fixture')
