from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import IncorrectMarkParenthesesStyle
from flake8_pytest_style.visitors import MarksVisitor


def test_ok_no_parameters():
    code = """
        import pytest

        @pytest.mark.foo()
        def test_something():
            pass
    """
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_parameters():
    code = """
        import pytest

        @pytest.mark.foo(scope='module')
        def test_something():
            pass
    """
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_without_parens():
    code = """
        import pytest

        @pytest.mark.foo
        def test_something():
            pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_not_error(MarksVisitor, code, config=config)


def test_ok_class():
    code = """
        import pytest

        @pytest.mark.foo()
        class TestClass:
            def test_something():
                pass
    """
    assert_not_error(MarksVisitor, code, config=DEFAULT_CONFIG)


def test_ok_class_without_parens():
    code = """
        import pytest

        @pytest.mark.foo
        class TestClass:
            def test_something():
                pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_not_error(MarksVisitor, code, config=config)


def test_error_without_parens():
    code = """
        import pytest

        @pytest.mark.foo
        def test_something():
            pass
    """
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=DEFAULT_CONFIG,
        mark_name='foo',
        expected_parens='()',
        actual_parens='',
    )


def test_error_with_parens():
    code = """
        import pytest

        @pytest.mark.foo()
        def test_something():
            pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=config,
        mark_name='foo',
        expected_parens='',
        actual_parens='()',
    )


def test_error_class_without_parens():
    code = """
        import pytest

        @pytest.mark.foo
        class TestClass:
            def test_something():
                pass
    """
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=DEFAULT_CONFIG,
        mark_name='foo',
        expected_parens='()',
        actual_parens='',
    )


def test_error_class_with_parens():
    code = """
        import pytest

        @pytest.mark.foo()
        class TestClass:
            def test_something():
                pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=False)
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=config,
        mark_name='foo',
        expected_parens='',
        actual_parens='()',
    )
