from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import MissingFixtureNameUnderscore
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_simple():
    code = """
        import pytest

        @pytest.fixture()
        def _patch_something(mocker):
            mocker.patch('some.thing')
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_return():
    code = """
        import pytest

        @pytest.fixture()
        def _patch_something(mocker):
            if something:
                return
            mocker.patch('some.thing')
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def _activate_context():
            with context:
                yield
    """
    assert_not_error(PytestStyleVisitor, code, config=DEFAULT_CONFIG)


def test_error_simple():
    code = """
        import pytest

        @pytest.fixture()
        def patch_something(mocker):
            mocker.patch('some.thing')
    """
    assert_error(
        PytestStyleVisitor,
        code,
        MissingFixtureNameUnderscore,
        name='patch_something',
        config=DEFAULT_CONFIG,
    )


def test_error_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def activate_context():
            with context:
                yield
    """
    assert_error(
        PytestStyleVisitor,
        code,
        MissingFixtureNameUnderscore,
        name='activate_context',
        config=DEFAULT_CONFIG,
    )
