DJANGO_SETTINGS_MODULE := gt_project.settings.dev

.PHONY: devserver qa lint lint_python lint_js isort isort_python tests tests_python tests_js spec spec_python


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

devserver:
	pipenv run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

shell:
	pipenv run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

messages:
	pipenv run python manage.py makemessages --no-wrap --no-location -l en -l fr
	pipenv run python manage.py makemessages --no-wrap --no-location -l en -l fr -d djangojs --ignore="gt/static/build_dev/*" --ignore="node_modules/*"

compiledmessages:
	pipenv run python manage.py compilemessages  -l en -l fr

init:
	pip install pipenv
	pipenv lock
	pipenv install --dev --three
	npm install


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort

# Code quality checks (eg. flake8, eslint, etc).
lint: lint_python lint_js
lint_python:
	pipenv run flake8
lint_js:
	npm run lint

# Import sort checks.
isort: isort_python
isort_python:
	pipenv run isort --check-only --recursive --diff gt gt_project


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

# Just runs all the tests!
tests: tests_python tests_js
tests_python:
	pipenv run py.test
tests_js:
	npm test

# Collects code coverage data.
coverage: coverage_python coverage_js
coverage_python:
	pipenv run py.test --cov-report term-missing --cov gt
coverage_js:
	npm test

# Run the tests in "spec" mode.
spec: spec_python
spec_python:
	pipenv run py.test --spec -p no:sugar
