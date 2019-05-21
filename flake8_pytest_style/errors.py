from ._vendor.flake8_plugin_utils import Error


class MissingFixtureParentheses(Error):
    code = 'PT001'
    message = 'you should use @pytest.fixture() over @pytest.fixture()'


class ExtraneousScopeFunction(Error):
    code = 'PT002'
    message = "scope='function' is implied in @pytest.fixture()"


class MissingFixtureNameUnderscore(Error):
    code = 'PT003'
    message = "fixture '{name}' does not return anything, add leading underscore"


class IncorrectFixtureNameUnderscore(Error):
    code = 'PT004'
    message = "fixture '{name}' returns a value, remove leading underscore"


class ParametrizeMultipleWithoutTuple(Error):
    code = 'PT005'
    message = (
        "test function '{name}' has comma-separated names "
        'in @pytest.mark.parametrize, use a tuple'
    )


class ParametrizeWrongType(Error):
    code = 'PT006'
    message = 'use only tuples in @pytest.mark.parametrize'


class PatchWithLambda(Error):
    code = 'PT007'
    message = 'use return_value= instead of patching with lambda'
