# flake8-pytest-style

[![pypi](https://badge.fury.io/py/flake8-pytest-style.svg)](https://pypi.org/project/flake8-pytest-style)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-pytest-style)
[![Downloads](https://img.shields.io/pypi/dm/flake8-pytest-style.svg)](https://pypistats.org/packages/flake8-pytest-style)
[![Build Status](https://github.com/m-burst/flake8-pytest-style/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/m-burst/flake8-pytest-style/actions/workflows/ci.yml)
[![Code coverage](https://codecov.io/gh/m-burst/flake8-pytest-style/branch/master/graph/badge.svg)](https://codecov.io/gh/m-burst/flake8-pytest-style)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Description

A `flake8` plugin checking common style issues or inconsistencies with `pytest`-based tests.

Currently the following errors are reported:

| Code    | Description |
| ------- | ----------- |
| [PT001] | use @pytest.fixture() over @pytest.fixture <br> (configurable by `pytest-fixture-no-parentheses`) |
| [PT002] | configuration for fixture '{name}' specified via positional args, use kwargs |
| [PT003] | scope='function' is implied in @pytest.fixture() |
| [PT004] | fixture '{name}' does not return anything, add leading underscore |
| [PT005] | fixture '{name}' returns a value, remove leading underscore |
| [PT006] | wrong name(s) type in @pytest.mark.parametrize, expected {expected_type} <br> (configurable by `pytest-parametrize-names-type`) |
| [PT007] | wrong values type in @pytest.mark.parametrize, expected {expected_type} <br> (configurable by `pytest-parametrize-values-type` and `pytest-parametrize-values-row-type`) |
| [PT008] | use return_value= instead of patching with lambda |
| [PT009] | use a regular assert instead of unittest-style '{assertion}' |
| [PT010] | set the expected exception in pytest.raises() |
| [PT011] | set the match parameter in pytest.raises({exception}) <br> (configurable by `pytest-raises-require-match-for`) |
| [PT012] | pytest.raises() block should contain a single simple statement |
| [PT013] | found incorrect import of pytest, use simple 'import pytest' instead |
| [PT014] | found duplicate test cases {indexes} in @pytest.mark.parametrize |
| [PT015] | assertion always fails, replace with pytest.fail() |
| [PT016] | no message passed to pytest.fail() |
| [PT017] | found assertion on exception {name} in except block, use pytest.raises() instead |
| [PT018] | assertion should be broken down into multiple parts |
| [PT019] | fixture {name} without value is injected as parameter, use @pytest.mark.usefixtures instead |
| [PT020] | @pytest.yield_fixture is deprecated, use @pytest.fixture |
| [PT021] | use yield instead of request.addfinalizer |
| [PT022] | no teardown in fixture {name}, use return instead of yield |
| [PT023] | use @pytest.mark.foo() over @pytest.mark.foo <br> (configurable by `pytest-mark-no-parentheses`) |
| [PT024] | pytest.mark.asyncio is unnecessary for fixtures |
| [PT025] | pytest.mark.usefixtures has no effect on fixtures |

## Installation

    pip install flake8-pytest-style

## Configuration

The plugin has the following configuration options:

* `pytest-fixture-no-parentheses` &mdash; see [PT001]
* `pytest-parametrize-names-type` &mdash; see [PT006]
* `pytest-parametrize-values-type` &mdash; see [PT007]
* `pytest-parametrize-values-row-type` &mdash; see [PT007]
* `pytest-raises-require-match-for` &mdash; see [PT011]
* `pytest-mark-no-parentheses` &mdash; see [PT023]

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

* add [PT025] (checks for erroneous `pytest.mark.usefixtures` on fixtures)

**1.4.4 - 2021-06-17**

* fix [PT023] not checking marks in classes
* fix [PT004] incorrectly firing on fixtures with `yield from`

**1.4.2 - 2021-05-24**

* update `flake8-plugin-utils` version to improve stability

**1.4.1 - 2021-04-01**

* fix argparse-related warnings

**1.4.0 - 2021-03-14**

* add [PT023] (checks for parentheses consistency in `pytest.mark` usage)
* add [PT024] (checks for unnecessary `pytest.mark.asyncio` on fixtures)
* fix [PT004], [PT005] firing on abstract fixtures
* fix [PT012] firing on `with` statements containing a single `pass`

**1.3.0 - 2020-08-30**

* add [PT022] (checks for `yield` fixtures without teardown)

**1.2.3 - 2020-08-06**

* update `flake8-plugin-utils` dependency to fix encoding problems on Windows

**1.2.2 - 2020-07-23**

* fix [PT004]/[PT005] inspecting returns of nested functions

**1.2.1 - 2020-06-15**

* fix [PT021] for factory fixtures (#46)

**1.2.0 - 2020-06-12**

* support scoped `mocker` fixtures from `pytest-mock` for [PT008]
* check for positional-only lambda arguments in [PT008]
* add [PT020] (checks for `pytest.yield_fixture`)
* add [PT021] (checks for `request.addfinalizer`)
* add documentation pages for all rules

**1.1.1 - 2020-04-17**

* fix [PT011] not reporting `match=''` as a violation

**1.1.0 - 2020-04-14**

* add [PT015] (checks for `assert False`)
* add [PT016] (checks for `pytest.fail()` without message)
* add [PT017] (checks for assertions on exceptions in `except` blocks)
* add [PT018] (checks for composite assertions)
* add [PT019] (checks for fixtures without value injected as parameters)

**1.0.0 - 2020-03-26**

* add [PT014] (checks for duplicate test cases in `@pytest.mark.parametrize`)

**0.6.0 - 2020-03-21**

* add configuration option `pytest-parametrize-names-type` for [PT006]
* add configuration options `pytest-parametrize-values-type` and
`pytest-parametrize-values-row-type` for [PT007]

**0.5.0 - 2020-03-09**

* add configuration option `pytest-fixture-no-parentheses` for [PT001]
* add [PT013] (checks for `from`-imports from `pytest`)

**0.4.0 - 2020-03-09**

* add [PT012] (checks for multiple statements in `with pytest.raises()`)

**0.3.1 - 2020-03-09**

* fix default value of `pytest-raises-require-match-for` config option

**0.3.0 - 2020-03-09**

* add [PT010] and [PT011] (checks for `pytest.raises` parameters)

**0.2.0 - 2020-03-01**

* add [PT009] (ported from [flake8-pytest](https://github.com/vikingco/flake8-pytest))

**0.1.3 - 2019-05-24**

* add `yield` fixtures support
* fix changelog entry for 0.1.2

**0.1.2 - 2019-05-23**

* fix parametrize checkers not working in decorators

**0.1.1 - 2019-05-23**

* update PyPI description

**0.1.0 - 2019-05-23**

* initial

[PT001]: /docs/rules/PT001.md
[PT002]: /docs/rules/PT002.md
[PT003]: /docs/rules/PT003.md
[PT004]: /docs/rules/PT004.md
[PT005]: /docs/rules/PT005.md
[PT006]: /docs/rules/PT006.md
[PT007]: /docs/rules/PT007.md
[PT008]: /docs/rules/PT008.md
[PT009]: /docs/rules/PT009.md
[PT010]: /docs/rules/PT010.md
[PT011]: /docs/rules/PT011.md
[PT012]: /docs/rules/PT012.md
[PT013]: /docs/rules/PT013.md
[PT014]: /docs/rules/PT014.md
[PT015]: /docs/rules/PT015.md
[PT016]: /docs/rules/PT016.md
[PT017]: /docs/rules/PT017.md
[PT018]: /docs/rules/PT018.md
[PT019]: /docs/rules/PT019.md
[PT020]: /docs/rules/PT020.md
[PT021]: /docs/rules/PT021.md
[PT022]: /docs/rules/PT022.md
[PT023]: /docs/rules/PT023.md
[PT024]: /docs/rules/PT024.md
[PT025]: /docs/rules/PT025.md
