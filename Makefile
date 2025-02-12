format:
	isort src/
	isort tests/
	black src/
	black tests/

tests: tests_python

check:
	isort src --check
	isort tests --check
	flake8 src
	flake8 tests
	black src --check
	black tests --check

tests_python:
	pytest --cov-report xml --cov src tests
