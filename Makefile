.PHONY: init lint isort coverage spec

init:
	pip install pipenv
	pipenv lock
	pipenv install --dev

lint:
	pipenv run flake8

isort:
	pipenv run isort --check-only --recursive --diff gt tests

coverage:
	pipenv run py.test --cov-report term-missing --cov gt

spec:
	pipenv run py.test --spec -p no:sugar
