format:
	poetry run isort src/
	poetry run isort tests/
	poetry run black src/
	poetry run black tests/

tests: tests_python

check:
	poetry run isort src --check
	poetry run isort tests --check
	poetry run flake8 src
	poetry run flake8 tests
	poetry run black src --check
	poetry run black tests --check

tests_python:
	poetry run pytest --cov-report xml --cov src tests
