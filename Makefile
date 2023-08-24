PYTHON := $(shell cat src/newsfeed/python_path.txt)
VENV_PATH := $(USERPROFILE)/venv
VENV_ACTIVATE := $(VENV_PATH)/Scripts/activate

install_dependencies:
	"$(PYTHON)" -m venv "$(VENV_PATH)"
	. "$(VENV_ACTIVATE)" && pip install -r requirements.txt
	. "$(VENV_ACTIVATE)" && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit

run_precommit:
	. "$(VENV_ACTIVATE)" && pre-commit run --all-files

run_tests:
	. "$(VENV_ACTIVATE)" && pytest tests/
