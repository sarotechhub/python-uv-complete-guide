# Basic Project Example

A simple Python project demonstrating basic uv usage patterns.

## Features

- Simple CLI application using Click
- HTTP requests with requests library
- Unit tests with pytest
- Development dependencies separated

## Getting Started

### Install dependencies

```bash
uv sync
```

### Run the project

```bash
# Using the installed script
uv run hello --name Alice --count 2

# Or directly with Python
uv run python main.py --name Bob
```

### Run tests

```bash
uv run pytest
uv run pytest --cov
```

### Format code

```bash
uv run black .
uv run ruff check .
```

## Project Structure

```
basic_project/
├── pyproject.toml      # Project configuration
├── main.py             # Main application
├── test_main.py        # Unit tests
└── README.md          # This file
```

## uv Commands Explained

- `uv sync` - Install all dependencies (including dev)
- `uv run` - Execute Python with the project environment
- `uv add package_name` - Add a new dependency
- `uv remove package_name` - Remove a dependency
- `uv lock` - Generate lock file for reproducibility

## Next Steps

- Explore dependency groups in more complex projects
- Add pre-commit hooks for quality checks
- Set up CI/CD with GitHub Actions
