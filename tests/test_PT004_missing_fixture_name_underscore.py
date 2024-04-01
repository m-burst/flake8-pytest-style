from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import MissingFixtureNameUnderscore
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_simple():
    code = """
        import pytest

        @pytest.fixture
        def _patch_something(mocker):
            mocker.patch('some.thing')
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_return():
    code = """
        import pytest

        @pytest.fixture
        def _patch_something(mocker):
            if something:
                return
            mocker.patch('some.thing')
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_yield():
    code = """
        import pytest

        @pytest.fixture
        def _activate_context():
            with context:
                yield
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_abstract_with_import_abc():
    code = """
        import abc

        import pytest

        class BaseTest:
            @pytest.fixture
            @abc.abstractmethod
            def my_fixture():
                raise NotImplementedError
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_abstract_with_from_import():
    code = """
        from abc import abstractmethod

        import pytest

        class BaseTest:
            @pytest.fixture
            @abstractmethod
            def my_fixture():
                raise NotImplementedError
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_ignoring_yield_from():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            yield from some_generator()
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_simple():
    code = """
        import pytest

        @pytest.fixture
        def patch_something(mocker):
            mocker.patch('some.thing')
    """
    assert_error(
        FixturesVisitor,
        code,
        MissingFixtureNameUnderscore,
        name='patch_something',
        config=DEFAULT_CONFIG,
    )


def test_error_with_yield():
    code = """
        import pytest

        @pytest.fixture
        def activate_context():
            with context:
                yield
    """
    assert_error(
        FixturesVisitor,
        code,
        MissingFixtureNameUnderscore,
        name='activate_context',
        config=DEFAULT_CONFIG,
    )
