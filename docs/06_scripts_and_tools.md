# Running Python Scripts and Tools with uv

Master script execution, entry points, and tool integration.

## The `uv run` Command

### Basic Script Execution

The fundamental way to run Python code with uv:

```bash
# Run a script
uv run python script.py

# Run with arguments
uv run python script.py --verbose --output results.json

# Run Python code directly
uv run python -c "print('Hello from uv')"

# Run interactive Python
uv run python  # Interactive interpreter
```

**What happens:**
1. uv activates the project's virtual environment
2. Runs Python with your command
3. Deactivates when done (transparent)

### Why `uv run` Over `python`?

```bash
# Without uv (requires manual activation)
source .venv/bin/activate
python script.py
deactivate

# With uv (automatic)
uv run python script.py

# Less ceremony, fewer mistakes!
```

## Running Installed Tools

### Using pip-based Tools

When you install tools via pip, use them with `uv run`:

```bash
# Install a tool
uv add --group dev black

# Run the tool
uv run black src/

# Instead of:
# source .venv/bin/activate
# black src/
# deactivate
```

### Running Multiple Tools

```bash
# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Type check
uv run mypy src/

# Run tests
uv run pytest

# Each command automatically uses .venv/
```

### Tool Versions

Using uv ensures consistent tool versions:

```bash
# pyproject.toml has specific versions
[project.optional-dependencies]
dev = ["black==23.3.0", "ruff==0.0.285"]

# Everyone uses same versions
uv sync --group dev
uv run black src/  # Version 23.3.0 everywhere
```

## Project Scripts and Entry Points

### Adding Scripts to pyproject.toml

Define custom commands in your project:

```toml
[project.scripts]
# Format: name = "module:function"
myapp = "my_app.cli:main"
myapp-admin = "my_app.admin:main"
serve = "my_app.server:run"
```

### Running Scripts

```bash
# Simple execution
uv run myapp

# With arguments
uv run myapp --help
uv run myapp config --set debug=true

# Admin commands
uv run myapp-admin --reset-db

# Start server
uv run serve --port 8080
```

### Example CLI with Scripts

```bash
# Create CLI project
uv init cli_tool
cd cli_tool

# Add click for CLI framework
uv add click

# Create main.py
cat > main.py << 'EOF'
import click

@click.command()
@click.option('--name', default='World', help='Name to greet')
@click.option('--count', default=1, help='Number of greetings')
def hello(name, count):
    """Simple program that greets NAME COUNT times."""
    for _ in range(count):
        click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    hello()
EOF

# Update pyproject.toml
cat >> pyproject.toml << 'EOF'

[project.scripts]
hello = "main:hello"
EOF

# Run script
uv run hello --name Alice --count 3
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run specific file
uv run pytest tests/test_unit.py

# Run specific test
uv run pytest tests/test_unit.py::test_addition

# Verbose output
uv run pytest -v
```

### Test Configuration

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --tb=short"
```

Then run simply:

```bash
# Uses pytest configuration from pyproject.toml
uv run pytest
```

### Running with Coverage

```bash
# Install coverage tool
uv add --group dev pytest pytest-cov

# Run with coverage
uv run pytest --cov=my_app tests/

# Generate HTML report
uv run pytest --cov=my_app --cov-report=html tests/

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Running Web Applications

### FastAPI Example

```bash
# Create API project
uv init api
cd api

# Add FastAPI and Uvicorn
uv add fastapi uvicorn[standard]

# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
EOF

# Run development server
uv run uvicorn main:app --reload
# Server runs at http://localhost:8000

# Run with specific port
uv run uvicorn main:app --port 8080 --reload
```

### Django Example

```bash
# Create Django project
uv init django_app
cd django_app

# Add Django
uv add django

# Create Django project
uv run django-admin startproject myproject .

# Create app
uv run python manage.py startapp myapp

# Run development server
uv run python manage.py runserver

# With port specification
uv run python manage.py runserver 8080
```

### Flask Example

```bash
# Setup
uv init flask_app
cd flask_app
uv add flask

# Create app.py
cat > app.py << 'EOF'
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
EOF

# Run server
uv run python app.py

# Or with flask command
uv run flask run --debug
```

## Working with Jupyter Notebooks

### Install and Run Jupyter

```bash
# Add Jupyter
uv add jupyter

# Start Jupyter Lab
uv run jupyter lab

# Start Jupyter Notebook
uv run jupyter notebook

# Specify port
uv run jupyter notebook --port 8888
```

### Jupyter in Project Environment

```bash
# Your notebook has access to project packages
# Example: if pyproject.toml has requests

# In notebook cell:
import requests
response = requests.get('https://api.example.com')

# Works because notebook runs in .venv/
```

## Python REPL and Interactive Shell

### Interactive Python Shell

```bash
# Start interactive Python
uv run python

# Now in Python interpreter with all packages
Python 3.11.0 | Packaged by conda-forge
>>> import requests
>>> requests.__version__
'2.31.0'
>>> exit()
```

### IPython for Better REPL

```bash
# Install IPython
uv add ipython

# Run enhanced REPL
uv run ipython

# Better syntax highlighting, tab completion, etc.
In [1]: import requests
In [2]: requests.__version__
Out[2]: '2.31.0'
```

## Running Multiple Commands

### Sequential Commands

```bash
# Run multiple operations
uv run black src/
uv run ruff check src/
uv run mypy src/
uv run pytest

# Each runs in the same .venv/
```

### Running in Series (with failure handling)

```bash
# Stop on first error
uv run python script1.py && \
uv run python script2.py && \
uv run python script3.py

# Continue even if one fails
uv run python script1.py || true
uv run python script2.py || true
```

### Make or Task Runners

Use Makefiles or task runners with uv:

```makefile
# Makefile
.PHONY: test lint format run

test:
	uv run pytest

lint:
	uv run ruff check src/

format:
	uv run black src/

run:
	uv run python main.py

all: lint test format
	@echo "All checks passed!"
```

Run with:
```bash
make test
make lint
make all
```

## Advanced Execution Patterns

### Running with Environment Variables

```bash
# Set environment for script
DEBUG=1 uv run python script.py

# Multiple variables
DEBUG=1 LOG_LEVEL=INFO uv run python app.py

# From .env file
export $(cat .env | xargs)
uv run python script.py
```

### Running with stdin/stdout

```bash
# Pipe input
echo "Alice" | uv run python script.py

# Redirect output
uv run python script.py > output.txt

# Pipe between commands
uv run python generate_data.py | uv run python process_data.py
```

### Running Python Modules

```bash
# Run as module (uses __main__.py)
uv run python -m my_package

# Install package in editable mode then run
uv add -e .
uv run python -m my_package

# With arguments
uv run python -m my_package --config config.json
```

### Profiling and Debugging

```bash
# Run with profiler
uv run python -m cProfile script.py

# Run with pdb debugger
uv run python -m pdb script.py

# Trace execution
uv run python -m trace --trace script.py

# Memory profiling (after installing memory_profiler)
uv add memory_profiler
uv run python -m memory_profiler script.py
```

## Running Other Programming Languages

### Running Compiled Extensions

```bash
# If your package has Rust/C extensions
uv add package_with_extensions

# Extensions are compiled and installed in .venv/
uv run python -c "import package_with_extensions"
```

## Shell Integration

### Shell Aliases (Optional)

```bash
# In ~/.bashrc or ~/.zshrc
alias pr='uv run python'
alias pt='uv run pytest'
alias pc='uv run python -c'

# Then use
pr script.py
pt --verbose
pc "import requests; print(requests.__version__)"
```

### Shell Completion

```bash
# bash completion (if available)
_uv_completion() {
  # completion logic
}
complete -o bashdefault -o default -o nospace -F _uv_completion uv
```

## Performance Tips

### Caching for Speed

```bash
# First run: installs and caches
uv run pytest

# Second run: uses cached packages (much faster)
uv run pytest

# Cached location
# ~/.cache/uv/ (Linux/macOS)
# %LOCALAPPDATA%\uv\Cache\ (Windows)
```

### Background Tasks

For long-running processes:

```bash
# Start server in background
uv run uvicorn main:app &

# Do other work
sleep 5

# Stop background process
kill %1  # Kill last background job

# Or use proper process manager
# docker-compose, systemd, supervisord, etc.
```

## Troubleshooting Script Execution

### Issue: "ModuleNotFoundError"

```bash
# Wrong environment

# Solution: Use uv run
uv run python script.py

# Not: 
# python script.py  (uses system Python)
```

### Issue: "Command not found"

```bash
# Tool not installed

# Solution: Install with uv
uv add tool_name

# Then run
uv run tool_name
```

### Issue: Script Hangs

```bash
# Usually: waiting for input

# Check script for input() calls
# Or redirect stdin:
echo "input_data" | uv run python script.py

# Add timeout
timeout 10 uv run python script.py
```

### Issue: Different Results Locally vs CI

```bash
# Environment mismatch

# Solution: Use lock file
# Commit uv.lock to git
uv sync  # Everyone gets same packages

# CI uses same lock file
```

## Real-World Example: Development Workflow

```bash
# Create project
uv init my_api
cd my_api

# Add dependencies
uv add fastapi uvicorn sqlalchemy
uv add --group dev pytest pytest-asyncio black ruff mypy

# Create API
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

# Format code
uv run black main.py

# Lint code
uv run ruff check main.py

# Type check
uv run mypy main.py

# Run tests (create tests/ first)
uv run pytest tests/

# Run development server
uv run uvicorn main:app --reload

# Production server would use:
# uv run gunicorn main:app -w 4
```

## Next Steps

- **Manage dependencies:** See [Dependency Management](04_dependency_management.md)
- **Project structure:** Jump to [Project Setup](03_project_setup.md)
- **Best practices:** Read [Best Practices](08_best_practices.md)

---

**Pro Tip:** `uv run` is your primary interface to Python. Use it for everything and let uv handle environment management! 🚀

