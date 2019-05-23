from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import ParametrizeValuesWrongType
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
            'name',
            ('a', 'b', 'c'),
        )
    """
    assert_error(
        PytestStyleVisitor, code, ParametrizeValuesWrongType, expected_type='list'
    )


def test_error_single_tuple_as_decorator():
    code = """
        import pytest

        @pytest.mark.parametrize(
            'name',
            ('a', 'b', 'c'),
        )
        def test_smth(name):
            pass
    """
    assert_error(
        PytestStyleVisitor, code, ParametrizeValuesWrongType, expected_type='list'
    )


def test_error_multiple_tuple():
    code = """
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            (
                ('a', 'b'),
                ('c', 'd'),
            ),
        )
    """
    assert_error(
        PytestStyleVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type='list of tuples',
    )


def test_error_inner_list():
    code = """
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            [
                ('a', 'b'),
                ['c', 'd'],
            ],
        )
    """
    assert_error(
        PytestStyleVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type='list of tuples',
    )
