from flake8_plugin_utils import assert_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import DuplicateParametrizeTestCases
from flake8_pytest_style.visitors import ParametrizeVisitor


def test_error():
    code = """
        pytest.mark.parametrize(
            'name',
            [
                {1: 2, 3: {*other_set, 4, 5}, **otherdict},
                {x: y},
                {3: {5, *other_set, 4}, 1: 2, **otherdict},
            ]
        )
    """
    assert_error(
        ParametrizeVisitor,
        code,
        DuplicateParametrizeTestCases,
        indexes=(1, 3),
        config=DEFAULT_CONFIG,
    )
