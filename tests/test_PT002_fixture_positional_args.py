from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import FixturePositionalArgs
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_no_args():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code)


def test_ok_only_kwargs():
    code = """
        import pytest

        @pytest.fixture(scope='module')
        def my_fixture():
            return 0
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error_only_args():
    code = """
        import pytest

        @pytest.fixture('module')
        def my_fixture():
            return 0
    """
    assert_error(PytestStyleVisitor, code, FixturePositionalArgs, name='my_fixture')


def test_error_mixed():
    code = """
        import pytest

        @pytest.fixture('module', autouse=True)
        def my_fixture():
            return 0
    """
    assert_error(PytestStyleVisitor, code, FixturePositionalArgs, name='my_fixture')
