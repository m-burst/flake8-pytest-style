.PHONY: init test test-cov lint format

CODE = flake8_pytest_style
TEST = pytest --verbosity=2 --showlocals --strict --cov=$(CODE)

init:
	poetry install
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(TEST) -k "$(k)"

test-cov:
	$(TEST) --cov-report=html

lint:
	flake8 --jobs 4 --statistics --show-source $(CODE) tests
	pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	mypy $(CODE) tests
	black --target-version py36 --skip-string-normalization --check $(CODE) tests
	pytest --dead-fixtures --dup-fixtures

format:
	isort --apply --recursive $(CODE) tests
	black --target-version py36 --skip-string-normalization $(CODE) tests
	unify --in-place --recursive $(CODE) tests

bump_major:
	bumpversion major

bump_minor:
	bumpversion minor

bump_patch:
	bumpversion patch
