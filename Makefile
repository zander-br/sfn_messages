# Project

SRC_DIR := src
TESTS_DIR := tests


# Format

.PHONY: fmt

fmt:


# Lint

.PHONY: lint lint-uv-lock

lint: lint-uv-lock

lint-uv-lock:
	uv lock --check


# Tests

.PHONY: test

test:


# Clean

.PHONY: clean clean-build clean-pycache clean-python-tools dist-clean

clean: clean-build clean-pycache clean-python-tools

clean-build:
	rm -rf requirements.txt build dist

clean-pycache:
	find $(SRC_DIR) $(TESTS_DIR) -name '__pycache__' -exec rm -rf {} +
	find $(SRC_DIR) $(TESTS_DIR) -type d -empty -delete

clean-python-tools:

dist-clean: clean
	rm -rf .venv $(SRC_DIR)/*.egg-info
