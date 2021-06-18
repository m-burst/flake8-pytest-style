from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import ErroneousUseFixturesOnFixture
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_not_fixture():
    code = """
        import pytest

        @pytest.mark.usefixtures('a')
        def test_something():
            pass
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_before():
    code = """
        import pytest

        @pytest.mark.usefixtures('a')
        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        ErroneousUseFixturesOnFixture,
        config=DEFAULT_CONFIG,
    )


def test_error_after():
    code = """
        import pytest

        @pytest.fixture()
        @pytest.mark.usefixtures('a')
        def my_fixture():
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        ErroneousUseFixturesOnFixture,
        config=DEFAULT_CONFIG,
    )
