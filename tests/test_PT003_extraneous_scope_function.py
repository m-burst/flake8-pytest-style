from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import ExtraneousScopeFunction
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_no_scope():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_ok_other_scope():
    code = """
        import pytest

        @pytest.fixture(scope='module')
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_error():
    code = """
        import pytest

        @pytest.fixture(scope='function')
        def my_fixture():
            return 0
    """
    assert_error(
        PytestStyleVisitor, code, ExtraneousScopeFunction, config=DEFAULT_CONFIG
    )
