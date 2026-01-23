# Project

SRC_DIR := src
TESTS_DIR := tests


# Build

.PHONY: build

build:
	uv build


# Format

.PHONY: fmt

fmt:
	uv run ruff check --select I001 --fix $(SRC_DIR) $(TESTS_DIR)
	uv run ruff format $(SRC_DIR) $(TESTS_DIR)


# Lint

.PHONY: lint lint-uv-lock lint-ruff-format lint-ruff-check lint-mypy

lint: lint-uv-lock lint-ruff-format lint-ruff-check lint-mypy

lint-uv-lock:
	uv lock --check

lint-ruff-format:
	uv run ruff format --diff $(SRC_DIR) $(TESTS_DIR)

lint-ruff-check:
	uv run ruff check $(SRC_DIR) $(TESTS_DIR)

lint-mypy:
	uv run mypy --show-error-context --pretty $(SRC_DIR) $(TESTS_DIR)


# Tests

.PHONY: test test-pytest test-coverage-report

test: test-pytest

test-pytest .coverage: data/xsd
	uv run coverage run -m pytest $(TESTS_DIR)
	uv run coverage report -m

test-coverage-report: .coverage
	uv run coverage html


# Data

.PHONY: data

data: data/xsd

data/xsd: data/xsd.zip
	rm -rf data/xsd.tmp
	mkdir -p data/xsd.tmp
	cd data/xsd.tmp && unzip ../xsd.zip
	mv data/xsd.tmp $@

data/xsd.zip:
	curl -o $@ https://www.bcb.gov.br/content/estabilidadefinanceira/cedsfn/Catalogos/XSDDOCV511.zip


# Clean

.PHONY: clean clean-build clean-pycache clean-python-tools clean-data dist-clean

clean: clean-build clean-pycache clean-python-tools

clean-build:
	rm -rf requirements.txt build dist

clean-pycache:
	find $(SRC_DIR) $(TESTS_DIR) -name '__pycache__' -exec rm -rf {} +
	find $(SRC_DIR) $(TESTS_DIR) -type d -empty -delete

clean-python-tools:
	rm -rf .ruff_cache .mypy_cache .pytest_cache .coverage .coverage.* htmlcov

clean-data:
	rm -rf data/xsd data/xsd.zip

dist-clean: clean clean-data
	rm -rf .venv $(SRC_DIR)/*.egg-info
