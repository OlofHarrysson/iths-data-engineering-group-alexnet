PYTHON := $(shell cat src/newsfeed/python_path.txt)
SHELL := /bin/bash

install_dependencies:
	$(PYTHON) -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit

run_precommit:
	pre-commit run --all-files

run_tests:
	pytest tests/