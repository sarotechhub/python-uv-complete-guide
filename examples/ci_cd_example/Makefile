"""Makefile for local CI/CD simulation."""

.PHONY: help install sync format lint test coverage clean all

help:
	@echo "Available targets:"
	@echo "  install   - Install uv (if not already installed)"
	@echo "  sync      - Install dependencies"
	@echo "  format    - Format code with black"
	@echo "  lint      - Lint code with ruff"
	@echo "  test      - Run tests"
	@echo "  coverage  - Run tests with coverage report"
	@echo "  clean     - Clean up generated files"
	@echo "  all       - Run format, lint, and test"

install:
	@echo "Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh

sync:
	uv sync

format:
	uv run black .

lint:
	uv run ruff check .
	uv run ruff check . --fix

test:
	uv run pytest -v

coverage:
	uv run pytest --cov --cov-report=html --cov-report=term

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: format lint test
