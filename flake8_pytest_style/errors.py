from flake8_plugin_utils import Error


class MissingFixtureParentheses(Error):
    code = 'PT001'
    message = 'use @pytest.fixture() over @pytest.fixture'


class FixturePositionalArgs(Error):
    code = 'PT002'
    message = (
        "configuration for fixture '{name}' specified via positional args, use kwargs"
    )


class ExtraneousScopeFunction(Error):
    code = 'PT003'
    message = "scope='function' is implied in @pytest.fixture()"


class MissingFixtureNameUnderscore(Error):
    code = 'PT004'
    message = "fixture '{name}' does not return anything, add leading underscore"


class IncorrectFixtureNameUnderscore(Error):
    code = 'PT005'
    message = "fixture '{name}' returns a value, remove leading underscore"


class ParametrizeNamesWrongType(Error):
    code = 'PT006'
    message = 'wrong name(s) type in @pytest.mark.parametrize, expected {expected_type}'


class ParametrizeValuesWrongType(Error):
    code = 'PT007'
    message = 'wrong values type in @pytest.mark.parametrize, expected {expected_type}'


class PatchWithLambda(Error):
    code = 'PT008'
    message = 'use return_value= instead of patching with lambda'
