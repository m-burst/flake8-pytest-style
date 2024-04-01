from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import UnnecessaryAsyncioMarkOnFixture
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_not_fixture():
    code = """
        import pytest

        @pytest.mark.asyncio()
        async def test_something():
            pass
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_not_fixture_no_parens():
    code = """
        import pytest

        @pytest.mark.asyncio
        async def test_something():
            pass
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_before():
    code = """
        import pytest

        @pytest.mark.asyncio()
        @pytest.fixture
        async def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor, code, UnnecessaryAsyncioMarkOnFixture, config=DEFAULT_CONFIG
    )


def test_error_before_no_parens():
    code = """
        import pytest

        @pytest.mark.asyncio
        @pytest.fixture
        async def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor, code, UnnecessaryAsyncioMarkOnFixture, config=DEFAULT_CONFIG
    )


def test_error_after():
    code = """
        import pytest

        @pytest.fixture
        @pytest.mark.asyncio()
        async def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor, code, UnnecessaryAsyncioMarkOnFixture, config=DEFAULT_CONFIG
    )


def test_error_after_no_parens():
    code = """
        import pytest

        @pytest.fixture
        @pytest.mark.asyncio
        async def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor, code, UnnecessaryAsyncioMarkOnFixture, config=DEFAULT_CONFIG
    )
