import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import (
    DEFAULT_CONFIG,
    ParametrizeValuesRowType,
    ParametrizeValuesType,
)
from flake8_pytest_style.errors import ParametrizeValuesWrongType
from flake8_pytest_style.visitors import ParametrizeVisitor

VALUES_LIST = ["a", "b", "c"]
VALUES_TUPLE = ("a", "b", "c")
VALUES_LIST_OF_LISTS = [["a", "b"], ["c", "d"]]
VALUES_LIST_OF_TUPLES = [("a", "b"), ("c", "d")]
VALUES_TUPLE_OF_LISTS = (["a", "b"], ["c", "d"])
VALUES_TUPLE_OF_TUPLES = (("a", "b"), ("c", "d"))
VALUES_LIST_OF_MIXED = [["a", "b"], ("c", "d")]
VALUES_TUPLE_OF_MIXED = (["a", "b"], ("c", "d"))


def _get_expected_type_str(values_cfg_type, rows_cfg_type):
    return f"{values_cfg_type.value} of {rows_cfg_type.value}s"


@pytest.mark.parametrize(
    ("values_cfg_type", "values"),
    [
        (ParametrizeValuesType.LIST, VALUES_LIST),
        (ParametrizeValuesType.TUPLE, VALUES_TUPLE),
    ],
)
def test_ok_single(values_cfg_type, values):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            'name',
            {values!r},
        )
    """
    config = DEFAULT_CONFIG._replace(parametrize_values_type=values_cfg_type)
    assert_not_error(ParametrizeVisitor, code, config=config)


@pytest.mark.parametrize(
    ("values_cfg_type", "rows_cfg_type", "values"),
    [
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.LIST,
            VALUES_LIST_OF_LISTS,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.LIST,
            VALUES_TUPLE_OF_LISTS,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.TUPLE,
            VALUES_LIST_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.TUPLE,
            VALUES_TUPLE_OF_TUPLES,
        ),
    ],
)
def test_ok_multiple(values_cfg_type, rows_cfg_type, values):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            {values!r},
        )
    """
    config = DEFAULT_CONFIG._replace(
        parametrize_values_type=values_cfg_type,
        parametrize_values_row_type=rows_cfg_type,
    )
    assert_not_error(ParametrizeVisitor, code, config=config)


@pytest.mark.parametrize(
    ("values_cfg_type", "values"),
    [
        (ParametrizeValuesType.LIST, VALUES_TUPLE),
        (ParametrizeValuesType.TUPLE, VALUES_LIST),
    ],
)
def test_error_single(values_cfg_type, values):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            'name',
            {values!r},
        )
    """
    config = DEFAULT_CONFIG._replace(parametrize_values_type=values_cfg_type)
    assert_error(
        ParametrizeVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type=values_cfg_type.value,
        config=config,
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
        ParametrizeVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type="list",
        config=DEFAULT_CONFIG,
    )


@pytest.mark.parametrize(
    ("values_cfg_type", "rows_cfg_type", "values"),
    [
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.LIST,
            VALUES_LIST_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.LIST,
            VALUES_TUPLE_OF_LISTS,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.LIST,
            VALUES_TUPLE_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.LIST,
            VALUES_LIST_OF_LISTS,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.LIST,
            VALUES_LIST_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.LIST,
            VALUES_TUPLE_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.TUPLE,
            VALUES_LIST_OF_LISTS,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.TUPLE,
            VALUES_TUPLE_OF_LISTS,
        ),
        (
            ParametrizeValuesType.LIST,
            ParametrizeValuesRowType.TUPLE,
            VALUES_TUPLE_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.TUPLE,
            VALUES_LIST_OF_LISTS,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.TUPLE,
            VALUES_LIST_OF_TUPLES,
        ),
        (
            ParametrizeValuesType.TUPLE,
            ParametrizeValuesRowType.TUPLE,
            VALUES_TUPLE_OF_LISTS,
        ),
    ],
)
def test_error_multiple(values_cfg_type, rows_cfg_type, values):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            {values!r},
        )
    """
    config = DEFAULT_CONFIG._replace(
        parametrize_values_type=values_cfg_type,
        parametrize_values_row_type=rows_cfg_type,
    )
    assert_error(
        ParametrizeVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type=_get_expected_type_str(values_cfg_type, rows_cfg_type),
        config=config,
    )


@pytest.mark.parametrize("values_cfg_type", list(ParametrizeValuesType))
@pytest.mark.parametrize("rows_cfg_type", list(ParametrizeValuesRowType))
@pytest.mark.parametrize("values", [VALUES_LIST_OF_MIXED, VALUES_TUPLE_OF_MIXED])
def test_error_multiple_mixed(values_cfg_type, rows_cfg_type, values):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            ('name1', 'name2'),
            {values!r},
        )
    """
    config = DEFAULT_CONFIG._replace(
        parametrize_values_type=values_cfg_type,
        parametrize_values_row_type=rows_cfg_type,
    )
    assert_error(
        ParametrizeVisitor,
        code,
        ParametrizeValuesWrongType,
        expected_type=_get_expected_type_str(values_cfg_type, rows_cfg_type),
        config=config,
    )
