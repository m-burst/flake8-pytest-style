from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import ParametrizeNamesWrongType
from flake8_pytest_style.visitors import PytestStyleVisitor


def test_ok_single():
    code = """
        import pytest

        pytest.mark.parametrize(
            'name',
            ['a', 'b', 'c'],
        )
    """
    assert_not_error(PytestStyleVisitor, code)


def test_ok_multiple():
    code = """
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            [
                ('a', 'b'),
                ('c', 'd'),
            ],
        )
    """
    assert_not_error(PytestStyleVisitor, code)


def test_error_single_tuple():
    code = """
        import pytest

        pytest.mark.parametrize(
            ('name',),
            ['a', 'b', 'c'],
        )
    """
    assert_error(
        PytestStyleVisitor, code, ParametrizeNamesWrongType, expected_type='string'
    )


def test_error_multiple_string():
    code = """
        import pytest

        pytest.mark.parametrize(
            'name1,name2',
            [
                ('a', 'b'),
                ('c', 'd'),
            ],
        )
    """
    assert_error(
        PytestStyleVisitor, code, ParametrizeNamesWrongType, expected_type='tuple'
    )


def test_error_multiple_list():
    code = """
        import pytest

        pytest.mark.parametrize(
            ['name1', 'name2'],
            [
                ('a', 'b'),
                ('c', 'd'),
            ],
        )
    """
    assert_error(
        PytestStyleVisitor, code, ParametrizeNamesWrongType, expected_type='tuple'
    )
