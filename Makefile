format: format_python

tests: tests_python

check: check_python

format_python:
	poetry run isort .
	poetry run black .

check_python:
	poetry run isort . --check
	poetry run flake8 .
	poetry run black . --check

tests_python:
	echo "no tests"
