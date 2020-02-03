.PHONY: init test test-cov lint format

CODE = flake8_pytest_style
TEST = poetry run pytest --verbosity=2 --showlocals --strict --cov=$(CODE)

init:
	poetry install
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(TEST) -k "$(k)"

test-cov:
	$(TEST) --cov-report=html

lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE) tests
	poetry run pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE) tests
	poetry run black --target-version py36 --skip-string-normalization --check $(CODE) tests
	poetry run pytest --dead-fixtures --dup-fixtures

format:
	poetry run isort --apply --recursive $(CODE) tests
	poetry run black --target-version py36 --skip-string-normalization $(CODE) tests
	poetry run unify --in-place --recursive $(CODE) tests

bump_major:
	bumpversion major

bump_minor:
	bumpversion minor

bump_patch:
	bumpversion patch
