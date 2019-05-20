PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.dev

.PHONY: devserver qa lint lint_python isort isort_python tests tests_python spec spec_python


init:
	pipenv install --dev --three
	npm install
	cp -n .env.json.example .env.json


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

c: console
console:
	pipenv run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

s: server
server:
	pipenv run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

messages:
	pipenv run python manage.py makemessages --no-wrap --no-location -l en -l fr
	pipenv run python manage.py makemessages --no-wrap --no-location -l en -l fr -d djangojs --ignore="$(PROJECT_PACKAGE)/static/build_dev/*" --ignore="node_modules/*" --ignore="coverage/*"

compiledmessages:
	pipenv run python manage.py compilemessages  -l en -l fr

migrations:
	pipenv run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

migrate:
	pipenv run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

superuser:
	pipenv run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)

webpack_server:
	npm run gulp -- webpack-dev-server


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort type_checks

# Code quality checks (eg. flake8, etc).
lint: lint_python lint_js
lint_python:
	pipenv run flake8
lint_js:
	npm run lint

# Import sort checks.
isort: isort_python
isort_python:
	pipenv run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(PROJECT_CONFIGURATION_PACKAGE)

# Type checks.
type_checks: type_checks_python
type_checks_python:
	pipenv run mypy -p main


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

# Just runs all the tests!
t: tests
tests: tests_python tests_js
tests_python:
	pipenv run py.test
tests_js:
	npm test

# Collects code coverage data.
coverage: coverage_python coverage_js
coverage_python:
	pipenv run py.test --cov-report term-missing --cov $(PROJECT_PACKAGE)
coverage_js:
	npm test

# Run the tests in "spec" mode.
spec: spec_python
spec_python:
	pipenv run py.test --spec -p no:sugar
