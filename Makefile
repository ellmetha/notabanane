.PHONY: devserver init lint isort coverage spec

coverage:
	pipenv run py.test --cov-report term-missing --cov gt

devserver:
	pipenv run python manage.py runserver --settings=gt_project.settings.dev

init:
	pip install pipenv
	pipenv lock
	pipenv install --dev

isort:
	pipenv run isort --check-only --recursive --diff gt tests

lint:
	pipenv run flake8

spec:
	pipenv run py.test --spec -p no:sugar
