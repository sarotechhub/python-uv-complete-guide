# CI/CD Example Project

A complete CI/CD setup example demonstrating best practices with uv, GitHub Actions, and local testing.

## Features

- GitHub Actions workflow for automated testing
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11, 3.12)
- Code quality checks (linting, formatting, type checking)
- Test coverage reporting
- Makefile for local CI/CD simulation
- Security scanning integration

## Getting Started

### Install dependencies

```bash
uv sync
```

### Run tests locally

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov
```

### Run quality checks

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type check
uv run mypy .
```

### Using Makefile

```bash
# View available targets
make help

# Run all checks and tests
make all

# Run only tests
make test

# Generate coverage report
make coverage

# Clean up
make clean
```

## Project Structure

```
ci_cd_example/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions workflow
├── pyproject.toml              # Project configuration
├── Makefile                    # Local task automation
├── calculator.py               # Main module
├── test_calculator.py          # Tests
└── README.md                  # This file
```

## GitHub Actions Workflow

The CI/CD pipeline runs:

1. **Tests** on multiple Python versions
2. **Code Formatting** check with black
3. **Linting** with ruff
4. **Type Checking** with mypy
5. **Coverage** reporting to Codecov

### Triggering the Workflow

- Pushes to `main` and `develop` branches
- Pull requests to `main` and `develop` branches

### View Results

1. Go to **Actions** tab in GitHub
2. Click on the workflow run
3. View logs for each job

## Local Testing

Simulate the CI/CD pipeline locally:

```bash
# Install dependencies
uv sync

# Format check
uv run black --check .

# Lint
uv run ruff check .

# Type check
uv run mypy .

# Run tests with coverage
uv run pytest --cov --cov-report=html
```

## Coverage Report

Generate a detailed coverage report:

```bash
uv run pytest --cov --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Adding More Tools

### Security Scanning with Bandit

```bash
uv add --dev bandit
uv run bandit -r .
```

### Pre-commit Hooks

```bash
uv add --dev pre-commit
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: 0.1.0
    hooks:
      - id: ruff
```

Then run:
```bash
uv run pre-commit install
```

## Best Practices

1. **Commit often** - Small commits are easier to review
2. **Write tests first** - Test-driven development helps catch bugs early
3. **Keep dependencies up-to-date** - Regular updates help security
4. **Run locally before pushing** - Use `make all` to catch issues early
5. **Monitor coverage** - Aim for >80% coverage

## Troubleshooting

### Workflow fails on specific Python version

Check the error logs in GitHub Actions and fix compatibility issues.

### Tests fail locally but pass in CI

- Check Python version: `python --version`
- Clear cache: `uv clean`
- Reinstall: `uv sync --refresh`

### Coverage not reporting

Ensure `pytest-cov` is installed:
```bash
uv sync
```

## Next Steps

- Set up branch protection rules
- Add code review requirements
- Integrate with SonarQube for code quality metrics
- Add performance benchmarking
- Set up automated deployment
