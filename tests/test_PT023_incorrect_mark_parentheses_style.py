import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import IncorrectMarkParenthesesStyle
from flake8_pytest_style.visitors import MarksVisitor

_CONFIG_WITHOUT_PARENS = DEFAULT_CONFIG._replace(mark_parentheses=False)
_CONFIG_WITH_PARENS = DEFAULT_CONFIG._replace(mark_parentheses=True)


SAMPLES_WITHOUT_PARENTHESES = [
    pytest.param(
        """
            import pytest

            @pytest.mark.foo
            def test_something():
                pass
        """,
        id='function',
    ),
    pytest.param(
        """
            import pytest

            @pytest.mark.foo
            class TestClass:
                def test_something():
                    pass
        """,
        id='class',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                @pytest.mark.foo
                def test_something():
                    pass
        """,
        id='method',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                @pytest.mark.foo
                class TestNestedClass:
                    def test_something():
                        pass
        """,
        id='nested_class',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                class TestNestedClass:
                    @pytest.mark.foo
                    def test_something():
                        pass
        """,
        id='nested_class_method',
    ),
]

SAMPLES_WITH_PARENTHESES = [
    pytest.param(
        """
            import pytest

            @pytest.mark.foo()
            def test_something():
                pass
        """,
        id='function',
    ),
    pytest.param(
        """
            import pytest

            @pytest.mark.foo()
            class TestClass:
                def test_something():
                    pass
        """,
        id='class',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                @pytest.mark.foo()
                def test_something():
                    pass
        """,
        id='method',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                @pytest.mark.foo()
                class TestNestedClass:
                    def test_something():
                        pass
        """,
        id='nested_class',
    ),
    pytest.param(
        """
            import pytest

            class TestClass:
                class TestNestedClass:
                    @pytest.mark.foo()
                    def test_something():
                        pass
        """,
        id='nested_class_method',
    ),
]


@pytest.mark.parametrize('mark_parentheses', [True, False])
def test_ok_with_parameters_regardless_of_config(mark_parentheses: bool):
    code = """
        import pytest

        @pytest.mark.foo(scope='module')
        def test_something():
            pass
    """
    config = DEFAULT_CONFIG._replace(mark_parentheses=mark_parentheses)
    assert_not_error(MarksVisitor, code, config=config)


@pytest.mark.parametrize('code', SAMPLES_WITHOUT_PARENTHESES)
def test_ok_without_parens(code: str):
    assert_not_error(MarksVisitor, code, config=_CONFIG_WITHOUT_PARENS)


@pytest.mark.parametrize('code', SAMPLES_WITH_PARENTHESES)
def test_ok_with_parens(code: str):
    assert_not_error(MarksVisitor, code, config=_CONFIG_WITH_PARENS)


@pytest.mark.parametrize('code', SAMPLES_WITHOUT_PARENTHESES)
def test_error_without_parens(code: str):
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=_CONFIG_WITH_PARENS,
        mark_name='foo',
        expected_parens='()',
        actual_parens='',
    )


@pytest.mark.parametrize('code', SAMPLES_WITH_PARENTHESES)
def test_error_with_parens(code: str):
    assert_error(
        MarksVisitor,
        code,
        IncorrectMarkParenthesesStyle,
        config=_CONFIG_WITHOUT_PARENS,
        mark_name='foo',
        expected_parens='',
        actual_parens='()',
    )
