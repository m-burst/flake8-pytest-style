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

* `PT002 configuration for fixture '{name}' specified via positional args, use kwargs`  
e.g. `@pytest.fixture(scope='module')` is OK, and `@pytest.fixture('module')` is an error

* `PT003 scope='function' is implied in @pytest.fixture()`  
e.g. `@pytest.fixture(scope='function')` should be replaced with `@pytest.fixture()`

* `PT004 fixture '{name}' does not return anything, add leading underscore`

* `PT005 fixture '{name}' returns a value, remove leading underscore`

* `PT006 wrong name(s) type in @pytest.mark.parametrize, expected {expected_type}`  
e.g. `@pytest.mark.parametrize(('name1', 'name2'), ...)` is ok,
and `@pytest.mark.parametrize('name1,name2', ...)` is an error

* `PT007 wrong values type in @pytest.mark.parametrize, expected {expected_type}`

* `PT008 use return_value= instead of patching with lambda`  
e.g. `mocker.patch('target', return_value=7)` is OK,
and `mocker.patch('target', lambda *args: 7)` is an error

* `PT009 use a regular assert instead of unittest-style '{assertion}'`

* `PT010 set the match parameter in pytest.raises`  
e.g. `pytest.raises(ValueError, match='exception text')` is OK,
and `pytest.raises(ValueError)` is an error.
    * Since this is a fairly disruptive rule, it is by default off. 
      You can turn it on by specifying in your `setup.cfg` file 
      which exceptions you would like this rule to apply to.
      For example, the following configuration will make flake8 verify 
      that all `pytest.raises` that use `ValueError` or `TypeError` 
      should have a match parameter as well: 
        ```
        [flake8]
        ...
        no-bare-raises-exceptions = ValueError,TypeError
        ```

## Installation

    pip install flake8-pytest-style

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

### Unreleased

* add `PT010` (no bare raises)

%### 0.2.0 - 2020-03-01

* add `PT009` (ported from [flake8-pytest](https://github.com/vikingco/flake8-pytest))

### 0.1.3 - 2019-05-24

* add `yield` fixtures support
* fix changelog entry for 0.1.2

### 0.1.2 - 2019-05-23

* fix parametrize checkers not working in decorators

### 0.1.1 - 2019-05-23

* update PyPI description

### 0.1.0 - 2019-05-23

* initial
