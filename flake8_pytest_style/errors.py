from flake8_plugin_utils import Error


class IncorrectFixtureParenthesesStyle(Error):
    code = 'PT001'
    message = 'use @pytest.fixture{expected_parens} over @pytest.fixture{actual_parens}'


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


class UnittestAssertion(Error):
    code = 'PT009'
    message = "use a regular assert instead of unittest-style '{assertion}'"


class RaisesWithoutException(Error):
    code = 'PT010'
    message = 'set the expected exception in pytest.raises()'


class RaisesWithoutMatch(Error):
    code = 'PT011'
    message = 'set the match parameter in pytest.raises({exception})'


class RaisesWithMultipleStatements(Error):
    code = 'PT012'
    message = 'pytest.raises() block should contain a single simple statement'


class IncorrectPytestImport(Error):
    code = 'PT013'
    message = "found incorrect import of pytest, use simple 'import pytest' instead"
