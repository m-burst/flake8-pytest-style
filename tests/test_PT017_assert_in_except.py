from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import AssertInExcept
from flake8_pytest_style.visitors import RaisesVisitor


def test_ok():
    code = """
        def test_xxx():
            try:
                something()
            except Exception as e:
                something_else()

            with pytest.raises(ZeroDivisionError) as e:
                1 / 0
            assert e.value.message
    """
    assert_not_error(RaisesVisitor, code, config=DEFAULT_CONFIG)


def test_error():
    code = """
        def test_xxx():
            try:
                something()
            except Exception as e:
                assert e.message, 'blah blah'
    """
    assert_error(RaisesVisitor, code, AssertInExcept, name='e', config=DEFAULT_CONFIG)
