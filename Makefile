# Determine OS
ifeq ($(OS),Windows_NT)
	detected_OS := Windows
else
	detected_OS := $(shell uname)
endif

# Set Python command and virtual environment paths based on OS
ifeq ($(detected_OS),Windows)
	PYTHON := $(shell cat python_path.txt)
	VENV_PATH := $(USERPROFILE)/venv
	VENV_ACTIVATE := $(VENV_PATH)/Scripts/activate
else
	SHELL := /bin/bash
	PYTHON := python3.10
	VENV_PATH := ./venv
	VENV_ACTIVATE := $(VENV_PATH)/bin/activate
endif

install_dependencies:
ifeq ($(detected_OS),Windows)
	"$(PYTHON)" -m venv "$(VENV_PATH)"
	. "$(VENV_ACTIVATE)" && pip install -r requirements.txt
	. "$(VENV_ACTIVATE)" && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit
else
	$(PYTHON) -m venv $(VENV_PATH)
	source $(VENV_ACTIVATE) && pip install -r requirements.txt
	source $(VENV_ACTIVATE) && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit
endif

run_precommit:
	. "$(VENV_ACTIVATE)" && pre-commit run --all-files

run_tests:
	. "$(VENV_ACTIVATE)" && pytest tests/