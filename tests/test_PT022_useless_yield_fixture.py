from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import UselessYieldFixture
from flake8_pytest_style.visitors import FixturesVisitor

# Skipping basic OK tests because we have A LOT of valid fixtures in other
# test files


def test_ok_complex_logic():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            if some_condition:
                resource = acquire_resource()
                yield resource
                resource.release()
                return
            yield None
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error():
    code = """
        import pytest

        @pytest.fixture
        def my_fixture():
            resource = acquire_resource()
            yield resource
    """
    assert_error(
        FixturesVisitor,
        code,
        UselessYieldFixture,
        name="my_fixture",
        config=DEFAULT_CONFIG,
    )
