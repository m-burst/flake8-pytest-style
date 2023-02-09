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


class RaisesTooBroad(Error):
    code = 'PT011'
    message = (
        'pytest.raises({exception}) is too broad,'
        ' set the match parameter or use a more specific exception'
    )


class RaisesWithMultipleStatements(Error):
    code = 'PT012'
    message = 'pytest.raises() block should contain a single simple statement'


class IncorrectPytestImport(Error):
    code = 'PT013'
    message = "found incorrect import of pytest, use simple 'import pytest' instead"


class DuplicateParametrizeTestCases(Error):
    code = 'PT014'
    message = 'found duplicate test cases {indexes} in @pytest.mark.parametrize'


class AssertAlwaysFalse(Error):
    code = 'PT015'
    message = 'assertion always fails, replace with pytest.fail()'


class FailWithoutMessage(Error):
    code = 'PT016'
    message = 'no message passed to pytest.fail()'


class AssertInExcept(Error):
    code = 'PT017'
    message = (
        'found assertion on exception {name} in except block,'
        ' use pytest.raises() instead'
    )


class CompositeAssertion(Error):
    code = 'PT018'
    message = 'assertion should be broken down into multiple parts'


class FixtureParamWithoutValue(Error):
    code = 'PT019'
    message = (
        'fixture {name} without value is injected as parameter,'
        ' use @pytest.mark.usefixtures instead'
    )


class DeprecatedYieldFixture(Error):
    code = 'PT020'
    message = '@pytest.yield_fixture is deprecated, use @pytest.fixture'


class FixtureFinalizerCallback(Error):
    code = 'PT021'
    message = 'use yield instead of request.addfinalizer'


class UselessYieldFixture(Error):
    code = 'PT022'
    message = 'no teardown in fixture {name}, use return instead of yield'


class IncorrectMarkParenthesesStyle(Error):
    code = 'PT023'
    message = (
        'use @pytest.mark.{mark_name}{expected_parens}'
        ' over @pytest.mark.{mark_name}{actual_parens}'
    )


class UnnecessaryAsyncioMarkOnFixture(Error):
    code = 'PT024'
    message = 'pytest.mark.asyncio is unnecessary for fixtures'


class ErroneousUseFixturesOnFixture(Error):
    code = 'PT025'
    message = 'pytest.mark.usefixtures has no effect on fixtures'


class UseFixturesWithoutParameters(Error):
    code = 'PT026'
    message = 'useless pytest.mark.usefixtures without parameters'


class UnittestRaisesAssertion(Error):
    code = 'PT027'
    message = "use pytest.raises() instead of unittest-style '{assertion}'"
