# Creating a Python Project Using uv

This guide walks through initializing new projects, understanding `pyproject.toml`, and setting up virtual environments.

## Project Initialization

### Basic Project Creation

The fastest way to start a new Python project:

```bash
uv init my_project
cd my_project
```

This creates:

```
my_project/
├── pyproject.toml    # Project metadata & dependencies
├── README.md         # Basic README
├── .gitignore        # Git ignore file
├── .python-version   # Python version specification
└── src/
    └── my_project/
        └── __init__.py
```

### What Each File Does

#### `.python-version`
```
3.11
```
Specifies which Python version your project uses. uv will use this version when running commands.

#### `README.md`
```markdown
# my_project

A sample project created with uv.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run python -m my_project
```
```

Basic documentation for your project.

#### `.gitignore`
```
# Virtual environment
.venv/

# Cache
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
```

Prevents committing unnecessary files.

## Understanding pyproject.toml

The `pyproject.toml` is the heart of your project. Let's explore what uv creates:

```toml
[project]
name = "my_project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.8"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# uv-specific configuration
```

### Breakdown of Key Sections

#### `[project]` - Project Metadata

```toml
[project]
name = "my_project"           # Package name
version = "0.1.0"             # Semantic versioning
description = "..."           # One-line description
readme = "README.md"          # Points to README
requires-python = ">=3.8"     # Minimum Python version
authors = [
    {name = "Your Name", email = "you@example.com"}
]
license = {text = "MIT"}      # License type
keywords = ["python", "tool"] # Search keywords
classifiers = [               # PyPI categories
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
]
dependencies = [              # Runtime dependencies
    "requests>=2.28.0",
    "pydantic>=1.10.0",
]
```

#### `[project.optional-dependencies]` - Optional Features

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "mypy>=1.0",
]
docs = [
    "sphinx>=5.0",
    "sphinx-rtd-theme>=1.0",
]
```

Install specific extras:
```bash
uv add --extra dev my_project
uv add --extra docs my_project
```

#### `[project.scripts]` - CLI Entry Points

```toml
[project.scripts]
my-tool = "my_project.cli:main"
my-script = "my_project.scripts:run"
```

Create command-line tools:
```bash
uv run my-tool --help
uv run my-script --version
```

#### `[tool.uv]` - uv Configuration

```toml
[tool.uv]
# Support older Python versions
prerelease = "allow"

# Use specific Python when resolving
python-version = "3.11"

# Control dependency resolution
managed = true
```

## Advanced Project Setup

### Creating a Project with Specific Python Version

```bash
# Use Python 3.11
uv init --python 3.11 my_project

# Use specific Python path
uv init --python /usr/bin/python3.10 my_project

# Use latest Python 3.x
uv init --python 3 my_project
```

Check the `.python-version` file:

```bash
cat my_project/.python-version
# Output: 3.11
```

### Creating a Package vs Script Project

#### Package Project (with src layout)

```bash
uv init --package my_package
```

Structure:
```
my_package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
├── pyproject.toml
└── README.md
```

Good for libraries and distributable packages.

#### Script Project (simpler)

```bash
uv init my_script
```

Structure:
```
my_script/
├── my_script/
│   └── __init__.py
├── main.py
├── pyproject.toml
└── README.md
```

Good for simple scripts and applications.

### Using Project Templates

While uv doesn't have built-in templates, you can customize initialization:

```bash
# Create basic project
uv init my_project

# Modify pyproject.toml with your preferred structure
# Add dependencies upfront
```

## Virtual Environment Management

### Automatic Virtual Environment

uv automatically creates and manages virtual environments:

```bash
# Navigate to project
cd my_project

# First time you run a command
uv run python --version

# uv automatically:
# 1. Creates .venv/
# 2. Installs Python
# 3. Activates environment
# 4. Runs your command
```

### Viewing Environment Status

```bash
# Check if environment exists
ls -la .venv  # Linux/macOS
dir /a:h .venv  # Windows

# See what Python is active
uv run python --version

# Check installed packages in environment
uv run pip list
```

### Manual Environment Management

```bash
# Create environment explicitly
uv venv

# Activate (if needed for shell commands)
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Now you're in the venv
python --version
```

## Project Structure Patterns

### Standard Web Project (FastAPI)

```bash
uv init --package api_project

# Create structure
mkdir -p api_project/api/{routes,models,schemas}
mkdir api_project/tests
```

Resulting `pyproject.toml`:

```toml
[project]
name = "api_project"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.24.0",
]
```

### Data Science Project

```bash
uv init --package data_project
```

`pyproject.toml`:

```toml
[project]
name = "data_project"
requires-python = ">=3.9"
dependencies = [
    "pandas>=2.0",
    "numpy>=1.24",
    "scikit-learn>=1.3",
    "jupyter>=1.0",
]

[project.optional-dependencies]
viz = ["matplotlib>=3.7", "seaborn>=0.12"]
ml = ["xgboost>=2.0", "lightgbm>=4.0"]
```

### CLI Tool Project

```bash
uv init --package my_cli
```

`pyproject.toml`:

```toml
[project]
name = "my_cli"
version = "1.0.0"
dependencies = [
    "click>=8.1",
    "rich>=13.0",  # Pretty output
]

[project.scripts]
mycli = "my_cli.cli:main"
```

With `src/my_cli/cli.py`:

```python
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('--name', default='World')
def main(name):
    """Simple CLI tool."""
    console.print(f"Hello {name}!")

if __name__ == "__main__":
    main()
```

## Project Configuration Examples

### Minimal Configuration

```toml
[project]
name = "my_app"
version = "0.1.0"
requires-python = ">=3.8"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Production-Grade Configuration

```toml
[project]
name = "my_app"
version = "0.1.0"
description = "Production-ready application"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Dev Team", email = "dev@company.com"}
]
license = {text = "MIT"}

keywords = ["api", "data"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
]

dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

docs = [
    "sphinx>=6.0",
    "sphinx-rtd-theme>=1.2",
    "sphinx-autodoc-typehints>=1.23",
]

[project.scripts]
myapp = "my_app.cli:main"

[tool.uv]
managed = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_app"]
```

## Working with Multiple Projects

### Managing Multiple Projects

Each project has its own virtual environment:

```bash
# Project A
cd project_a
uv add requests

# Project B (separate environment)
cd ../project_b
uv add django

# Switch back to A
cd ../project_a
uv run python -c "import requests"  # Works in A's env
```

### Sharing Code Between Projects

```bash
# Develop two related packages
uv init --package core_lib
uv init --package web_app

# Add core_lib to web_app
cd web_app
uv add ../core_lib

# Now web_app imports from core_lib
```

## Troubleshooting Project Setup

### Issue: "pyproject.toml not found"

```bash
# Make sure you're in project directory
pwd  # or cd if needed

# Create one if missing
uv init .  # Initialize in current directory
```

### Issue: "Python version not found"

```bash
# Check available versions
uv python list

# Install specific version
uv python install 3.11

# Set in .python-version
echo "3.11" > .python-version
```

### Issue: "Virtual environment won't activate"

```bash
# uv activates automatically
uv run python script.py  # Works automatically

# Manual activation (rarely needed)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows

# Or recreate
rm -rf .venv
uv sync  # Recreates .venv
```

## Next Steps

Now that your project is created:

1. **Add Dependencies:** See [Dependency Management](04_dependency_management.md)
2. **Understand Environments:** Read [Virtual Environments](05_virtual_envs.md)
3. **Run Code:** Jump to [Scripts & Tools](06_scripts_and_tools.md)

## Complete Example

Here's a complete workflow:

```bash
# 1. Create project
uv init web_server

# 2. Navigate to it
cd web_server

# 3. Add dependencies
uv add fastapi uvicorn

# 4. Add dev dependencies
uv add --group dev pytest pytest-asyncio

# 5. Check pyproject.toml
cat pyproject.toml

# 6. Run Python
uv run python -c "import fastapi; print(fastapi.__version__)"

# 7. Run tests (when available)
uv run pytest

# 8. Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
EOF

# 9. Run server
uv run uvicorn main:app --reload
```

Your project is now set up and ready to develop! 🚀

