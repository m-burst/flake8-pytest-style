import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG, ParametrizeNamesType
from flake8_pytest_style.errors import ParametrizeNamesWrongType
from flake8_pytest_style.visitors import ParametrizeVisitor

NAMES_CSV = "name1,name2"
NAMES_LIST = ["name1", "name2"]
NAMES_TUPLE = ("name1", "name2")


def test_ok_single():
    code = """
        import pytest

        pytest.mark.parametrize(
            'name',
            ['a', 'b', 'c'],
        )
    """
    assert_not_error(ParametrizeVisitor, code, config=DEFAULT_CONFIG)


@pytest.mark.parametrize(
    ("cfg_type", "names"),
    [
        (ParametrizeNamesType.CSV, NAMES_CSV),
        (ParametrizeNamesType.LIST, NAMES_LIST),
        (ParametrizeNamesType.TUPLE, NAMES_TUPLE),
    ],
)
def test_ok_multiple(cfg_type, names):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            {names!r},
            [
                ('a', 'b'),
                ('c', 'd'),
            ],
        )
    """
    config = DEFAULT_CONFIG._replace(parametrize_names_type=cfg_type)
    assert_not_error(ParametrizeVisitor, code, config=config)


def test_error_single_tuple():
    code = """
        import pytest

        pytest.mark.parametrize(
            ('name',),
            ['a', 'b', 'c'],
        )
    """
    assert_error(
        ParametrizeVisitor,
        code,
        ParametrizeNamesWrongType,
        expected_type="string",
        config=DEFAULT_CONFIG,
    )


@pytest.mark.parametrize(
    ("cfg_type", "names"),
    [
        (ParametrizeNamesType.CSV, NAMES_LIST),
        (ParametrizeNamesType.CSV, NAMES_TUPLE),
        (ParametrizeNamesType.LIST, NAMES_CSV),
        (ParametrizeNamesType.LIST, NAMES_TUPLE),
        (ParametrizeNamesType.TUPLE, NAMES_CSV),
        (ParametrizeNamesType.TUPLE, NAMES_LIST),
    ],
)
def test_error_multiple(cfg_type, names):
    code = f"""
        import pytest

        pytest.mark.parametrize(
            {names!r},
            [
                ('a', 'b'),
                ('c', 'd'),
            ],
        )
    """
    config = DEFAULT_CONFIG._replace(parametrize_names_type=cfg_type)
    assert_error(
        ParametrizeVisitor,
        code,
        ParametrizeNamesWrongType,
        expected_type=cfg_type.value,
        config=config,
    )
