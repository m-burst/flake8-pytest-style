.PHONY: init test test-cov lint format

CODE = flake8_pytest_style
TEST = poetry run pytest --verbosity=2 --showlocals --strict-markers --cov=$(CODE)

init:
	poetry install
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(TEST) -k "$(k)"

test-cov:
	$(TEST) --cov-report=html

lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE) tests scripts
	poetry run pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE) tests scripts
	poetry run black --target-version py38 --skip-string-normalization --check $(CODE) tests scripts
	poetry run pytest --dead-fixtures --dup-fixtures

format:
	poetry run isort $(CODE) tests scripts
	poetry run black --target-version py38 --skip-string-normalization $(CODE) tests scripts
	poetry run unify --in-place --recursive $(CODE) tests scripts

bump_major:
	poetry run bumpversion major

bump_minor:
	poetry run bumpversion minor

bump_patch:
	poetry run bumpversion patch
