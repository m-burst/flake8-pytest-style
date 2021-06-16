from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import IncorrectFixtureNameUnderscore
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_with_return():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture(mocker):
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def activate_context():
            with get_context() as context:
                yield context
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_nested_function():
    code = """
        @pytest.fixture()
        def _any_fixture(mocker):
            def nested_function():
                return 1

            mocker.patch('...', nested_function)
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_abstract_with_import_abc():
    code = """
        import abc

        import pytest

        class BaseTest:
            @pytest.fixture()
            @abc.abstractmethod
            def _my_fixture():
                return NotImplemented
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_abstract_with_from_import():
    code = """
        from abc import abstractmethod

        import pytest

        class BaseTest:
            @pytest.fixture()
            @abstractmethod
            def _my_fixture():
                return NotImplemented
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_with_return():
    code = """
        import pytest

        @pytest.fixture()
        def _my_fixture(mocker):
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureNameUnderscore,
        name='_my_fixture',
        config=DEFAULT_CONFIG,
    )


def test_error_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def _activate_context():
            with get_context() as context:
                yield context
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureNameUnderscore,
        name='_activate_context',
        config=DEFAULT_CONFIG,
    )


def test_error_with_conditional_yield_from():
    code = """
        import pytest

        @pytest.fixture()
        def _activate_context():
            if some_condition:
                with get_context() as context:
                    yield context
            else:
                yield from other_context()
    """
    # since we have yield with value in one branch,
    # we assume that the fixture yields a value
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureNameUnderscore,
        name='_activate_context',
        config=DEFAULT_CONFIG,
    )
