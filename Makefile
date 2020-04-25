PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.development


init:
	@printf "${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Environment settings${RESET}\n\n"

	rsync --ignore-existing .env.json.example .env.json
	sed -i .bak "s/.*__whoami__.*/  \"DB_USER\": \"$(USER)\",/" .env.json
	rm -f .env.json.bak

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Python dependencies${RESET}\n\n"

	poetry env use 3.8
	poetry install

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Node.js dependencies${RESET}\n\n"

	npm install

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Initial assets build${RESET}\n\n"

	npm run gulp -- build

	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Database${RESET}\n\n"

	psql -l|awk '{print $1}'|grep -w notabanane || createdb notabanane 2>/dev/null
	poetry run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

	@printf "\n\n${YELLOW}---------------- Done.${RESET}\n\n"


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: c console
## Alias of "console".
c: console
## Launch a development console.
console:
	poetry run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: s server
## Alias of "server".
s: server
## Launch a development server.
server:
	env DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) poetry run uvicorn asgi:application --host 0.0.0.0 --reload --reload-dir ./

## Generate .po translations files.
messages:
	poetry run python manage.py makemessages --no-wrap --no-location -l en -l fr
	poetry run python manage.py makemessages --no-wrap --no-location -l en -l fr -d djangojs --ignore="$(PROJECT_PACKAGE)/static/build_dev/*" --ignore="node_modules/*" --ignore="coverage/*" --extension jsx

## Generate .mo compiled translations files.
compiledmessages:
	poetry run python manage.py compilemessages -l en -l fr

## Generates the GraphQL schema dump.
graphql_schema:
	poetry run python manage.py dump_graphql_schema -o project/db/schema.graphql

## Generate new database migrations.
migrations:
	poetry run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

.PHONY: migrate
## Run the database migrations.
migrate:
	poetry run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: superuser
## Create a superuser.
superuser:
	poetry run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: ws webpack_server
## Alias of "webpack_server".
ws: webpack_server
## Launch a webpack development server with hot reloading.
webpack_server:
	npm run gulp -- webpack-dev-server

## Generate or refresh poetry.lock and requirements.freeze
locked_requirements:
	poetry update
	poetry export -f requirements.txt > requirements.freeze


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: qa
## Trigger all quality assurance checks.
qa: lint isort

.PHONY: lint lint_python lint_python
## Trigger code quality checks (flake8, eslint).
lint: lint_python lint_js
## Trigger Python code quality checks (flake8).
lint_python:
	poetry run flake8
## Trigger Javascript code quality checks (eslint).
lint_js:
	npm run lint

.PHONY: isort isort_python
## Check Python imports sorting.
isort: isort_python
## Check Python imports sorting.
isort_python:
	poetry run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(PROJECT_CONFIGURATION_PACKAGE)


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

.PHONY: t tests tests_python tests_js
## Alias of "tests".
t: tests
## Run all the test suites.
tests: tests_python tests_js
## Run the Python test suite.
tests_python:
	poetry run py.test
## Run the Javascript test suite.
tests_js:
	npm test

.PHONY: coverage coverage_python coverage_js
## Collects code coverage data.
coverage: coverage_python coverage_js
## Collects code coverage data for the Python codebase.
coverage_python:
	poetry run py.test --cov-report term-missing --cov $(PROJECT_PACKAGE)
## Collects code coverage data for the Javascript codebase.
coverage_js:
	npm test

.PHONY: spec spec_python
# Run the test suites in "spec" mode.
spec: spec_python
# Run the Python test suite in "spec" mode.
spec_python:
	poetry run py.test --spec


# MAKEFILE HELPERS
# ~~~~~~~~~~~~~~~~
# The following rules can be used to list available commands and to display help messages.
# --------------------------------------------------------------------------------------------------

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help
## Print Makefile help.
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<action>${RESET}'
	@echo ''
	@echo 'Actions:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)-30s${RESET}\t${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -t'|' -sk1,1
