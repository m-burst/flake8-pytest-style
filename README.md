# flake8-pytest-style

[![pypi](https://badge.fury.io/py/flake8-pytest-style.svg)](https://pypi.org/project/flake8-pytest-style)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-pytest-style)
[![Downloads](https://img.shields.io/pypi/dm/flake8-pytest-style.svg)](https://pypistats.org/packages/flake8-pytest-style)
[![Build Status](https://travis-ci.com/m-burst/flake8-pytest-style.svg?branch=master)](https://travis-ci.com/m-burst/flake8-pytest-style)
[![Code coverage](https://codecov.io/gh/m-burst/flake8-pytest-style/branch/master/graph/badge.svg)](https://codecov.io/gh/m-burst/flake8-pytest-style)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Description

A `flake8` plugin checking common style issues or inconsistencies with `pytest`-based tests.

Currently the following errors are reported:

* `PT001 use @pytest.fixture() over @pytest.fixture`  
The preferred style is controlled by the configuration option
`pytest-fixture-no-parentheses`

* `PT002 configuration for fixture '{name}' specified via positional args, use kwargs`  
e.g. `@pytest.fixture(scope='module')` is OK, and `@pytest.fixture('module')` is an error

* `PT003 scope='function' is implied in @pytest.fixture()`  
e.g. `@pytest.fixture(scope='function')` should be replaced with `@pytest.fixture()`

* `PT004 fixture '{name}' does not return anything, add leading underscore`

* `PT005 fixture '{name}' returns a value, remove leading underscore`

* `PT006 wrong name(s) type in @pytest.mark.parametrize, expected {expected_type}`  
For a single name the expected type is always a plain string.
For multiple names the expected type is controlled by the configuration
variable `pytest-parametrize-names-type`.

* `PT007 wrong values type in @pytest.mark.parametrize, expected {expected_type}`
The expected type of the list of rows is controlled by the configuration
variable `pytest-parametrize-values-type`.
The expected type of each row in case of multiple arguments is controlled by
the configuration variable `pytest-parametrize-values-row-type`.

* `PT008 use return_value= instead of patching with lambda`  
e.g. `mocker.patch('target', return_value=7)` is OK,
and `mocker.patch('target', lambda *args: 7)` is an error

* `PT009 use a regular assert instead of unittest-style '{assertion}'`

* `PT010 set the expected exception in pytest.raises()`

* `PT011 set the match parameter in pytest.raises({exception})`  
e.g. `pytest.raises(ValueError, match='exception text')` is OK,
and `pytest.raises(ValueError)` is an error.  
The exception list is controlled by the configuration option 
`pytest-raises-require-match-for`.

* `PT012 pytest.raises() block should contain a single simple statement`  
this forbids multiple statements and control flow structures within
`pytest.raises()` blocks.

* `PT013 found incorrect import of pytest, use simple 'import pytest' instead`

* `PT014 found duplicate test cases {indexes} in @pytest.mark.parametrize`

## Installation

    pip install flake8-pytest-style
    
## Configuration

The plugin has the following configuration options:

* `pytest-fixture-no-parentheses`  
Boolean flag specifying whether `@pytest.fixture()` without parameters
should have parentheses, as checked by `PT001`.  
If the option is set to false (the default), `@pytest.fixture()` is valid
and `@pytest.fixture` is an error.  
If set to true, `@pytest.fixture` is valid and `@pytest.fixture()` is
an error.

* `pytest-parametrize-names-type`  
Expected type for multiple argument names in `@pytest.mark.parametrize`,
as checked by `PT006`. The following values are supported:
  * `csv` &mdash; a comma-separated list, e.g. `@pytest.mark.parametrize('name1,name2', ...)`
  * `tuple` (default) &mdash; e.g. `@pytest.mark.parametrize(('name1', 'name2'), ...)`
  * `list` &mdash; e.g. `@pytest.mark.parametrize(['name1', 'name2'], ...)`
  
* `pytest-parametrize-values-type`  
Expected type for the list of values rows in `@pytest.mark.parametrize`,
as checked by `PT007`. The following values are supported:
  * `tuple` &mdash; e.g. `@pytest.mark.parametrize('name', (1, 2, 3))`
  * `list` (default) &mdash; e.g. `@pytest.mark.parametrize('name', [1, 2, 3])`

* `pytest-parametrize-values-row-type`  
Expected type for each row of values in `@pytest.mark.parametrize` in case of
multiple parameters, as checked by `PT007`. The following values are supported:
  * `tuple` (default) &mdash; e.g. `@pytest.mark.parametrize(('name1', 'name2'), [(1, 2), (3, 4)])`
  * `list` &mdash; e.g. `@pytest.mark.parametrize(('name1', 'name2'), [[1, 2], [3, 4]])`

* `pytest-raises-require-match-for`  
Comma-separated list of exception names that require a `match=` parameter
in a `pytest.raises()` call, as checked by `PT011`. By default the list
contains the following exceptions:
  * `BaseException`, `Exception`
  * `ValueError`
  * `OSError`, `IOError`, `EnvironmentError`, `socket.error`

## For developers

### Install deps and setup pre-commit hook

    make init

### Run linters, autoformat, tests etc.

    make format lint test

### Bump new version

    make bump_major
    make bump_minor
    make bump_patch

## License

MIT

## Change Log

**Unreleased**

...

**1.0.0 - 2020-03-26**

* add `PT014` (checks for duplicate test cases in `@pytest.mark.parametrize`)

**0.6.0 - 2020-03-21**

* add configuration option `pytest-parametrize-names-type` for `PT006`
* add configuration options `pytest-parametrize-values-type` and
`pytest-parametrize-values-row-type` for `PT007`

**0.5.0 - 2020-03-09**

* add configuration option `pytest-fixture-no-parentheses` for `PT001`
* add `PT013` (checks for `from`-imports from `pytest`)

**0.4.0 - 2020-03-09**

* add `PT012` (checks for multiple statements in `with pytest.raises()`)

**0.3.1 - 2020-03-09**

* fix default value of `pytest-raises-require-match-for` config option

**0.3.0 - 2020-03-09**

* add `PT010` and `PT011` (checks for `pytest.raises` parameters)

**0.2.0 - 2020-03-01**

* add `PT009` (ported from [flake8-pytest](https://github.com/vikingco/flake8-pytest))

**0.1.3 - 2019-05-24**

* add `yield` fixtures support
* fix changelog entry for 0.1.2

**0.1.2 - 2019-05-23**

* fix parametrize checkers not working in decorators

**0.1.1 - 2019-05-23**

* update PyPI description

**0.1.0 - 2019-05-23**

* initial
