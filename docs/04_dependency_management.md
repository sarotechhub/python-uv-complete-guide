# Dependency Management with uv

Master adding, removing, and managing dependencies with precision and control.

## Adding Dependencies

### Basic Dependency Addition

The simplest way to add a package:

```bash
# Add latest version
uv add requests

# This:
# 1. Resolves the latest compatible version
# 2. Adds to pyproject.toml
# 3. Updates uv.lock with all transitive dependencies
# 4. Installs in .venv/
```

### Viewing What Was Added

```bash
# Check pyproject.toml
cat pyproject.toml
# Shows: dependencies = ["requests==2.31.0"]

# Check lock file
head -20 uv.lock
# Shows: precise versions and hashes

# Verify installation
uv run python -c "import requests; print(requests.__version__)"
```

### Adding Multiple Dependencies

```bash
# Add several at once
uv add requests flask sqlalchemy

# Add with version constraints
uv add "django>=4.0" "celery>=5.3" "redis>=4.5"

# Mix specific and flexible versions
uv add django requests "pandas>=2.0"
```

### Specifying Versions

#### Exact Version

```bash
# Install exact version
uv add "requests==2.31.0"

# pyproject.toml shows:
dependencies = ["requests==2.31.0"]

# Lock file contains exact version and hash
```

#### Compatible Release

```bash
# ~= allows patch updates only (recommended for stability)
uv add "django~=4.2"
# Allows: 4.2.0, 4.2.1, 4.2.5 but not 4.3.0

# pyproject.toml shows:
dependencies = ["django~=4.2"]
```

#### Minimum Version

```bash
# >= allows any newer version
uv add "requests>=2.28"
# Allows: 2.28.0, 2.29.0, 3.0.0, etc.

# Use when you need a feature from a specific version
```

#### Complex Constraints

```bash
# Combine multiple constraints
uv add "requests>=2.28,<3"
# Allows: 2.28.0, 2.29.0, 2.31.0 but not 3.0.0

# Multiple packages with different constraints
uv add "django>=4.0,<5" "celery>=5.0" "redis~=4.5"
```

## Dependency Groups

Organize dependencies by purpose (dev, test, docs, etc.).

### Adding Dev Dependencies

```bash
# Add to a group
uv add --group dev pytest pytest-cov black mypy

# pyproject.toml shows:
[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "black", "mypy"]
```

### Viewing Groups

```bash
# List all groups
uv pip show  # Shows installed packages

# See what's in each group
cat pyproject.toml | grep -A 5 "optional-dependencies"
```

### Common Dependency Groups

```toml
[project.optional-dependencies]
# Development tools
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]

# Documentation
docs = [
    "sphinx>=6.0",
    "sphinx-rtd-theme>=1.2",
]

# Data processing
data = [
    "pandas>=2.0",
    "numpy>=1.24",
    "scipy>=1.10",
]

# Visualization
viz = [
    "matplotlib>=3.7",
    "seaborn>=0.12",
    "plotly>=5.0",
]

# Performance/Production
perf = [
    "uvloop>=0.17",
    "orjson>=3.9",
]
```

### Using Optional Dependencies

Install specific groups when needed:

```bash
# Install with dev dependencies
uv sync --group dev

# Install with multiple groups
uv sync --group dev --group docs

# Install without dev dependencies
uv sync --no-group dev
```

## The `uv.lock` File

### Understanding Lock Files

The lock file is the **source of truth** for reproducibility:

```bash
# View lock file structure
cat uv.lock | head -50
```

Example `uv.lock` content:

```toml
version = 3

[[package]]
name = "requests"
version = "2.31.0"
source = { type = "registry", url = "..." }
sdist = { url = "...", hash = "sha256:..." }
wheels = [{url = "...", hash = "sha256:..."}]
requires-python = ">=3.7"

[[package]]
name = "charset-normalizer"
version = "3.3.2"
source = { type = "registry", url = "..." }
# ... and so on
```

### Why Lock Files Matter

**Reproducibility:**
```
Same uv.lock → Same environment → Same behavior
```

**Benefits:**

| Benefit | Impact |
|---------|--------|
| **Deterministic Builds** | CI/CD runs identical code every time |
| **Dependency Pinning** | No surprise version upgrades break code |
| **Security** | Know exactly what versions are installed |
| **Offline Installs** | Can install from lock file without PyPI |

### Lock File Workflow

```bash
# 1. Developer adds dependency
uv add new_package

# 2. uv.lock is created/updated automatically
# 3. Commit uv.lock to git
git add uv.lock
git commit -m "Add new_package"

# 4. Other developers/CI runs
uv sync  # Installs EXACTLY what's in lock file

# 5. Same environment everywhere ✅
```

### Regenerating Lock Files

```bash
# Update lock file without changing pyproject.toml
uv lock

# Force regenerate (useful if corrupted)
rm uv.lock
uv lock

# Update to latest compatible versions
uv lock --upgrade
```

## Updating Dependencies

### Updating Single Dependency

```bash
# Update to latest compatible version
uv add --upgrade requests

# This respects version constraints in pyproject.toml
# If you specified ~=2.31, it won't jump to 3.0
```

### Updating All Dependencies

```bash
# Upgrade all dependencies
uv lock --upgrade

# This checks for new versions and updates lock file
# Safe because respects version constraints

# pyproject.toml stays the same
# Only uv.lock changes
```

### Controlled Updates

```bash
# Update specific package
uv add --upgrade requests

# View what changed
git diff uv.lock | grep "version"

# Update to latest MAJOR versions (breaking changes)
uv lock --upgrade-package requests
```

## Removing Dependencies

### Basic Removal

```bash
# Remove package
uv remove requests

# This:
# 1. Removes from pyproject.toml
# 2. Updates uv.lock
# 3. Removes from .venv/

# Verify removal
uv run python -c "import requests" 2>&1 | grep -i error
```

### Removing from Groups

```bash
# Remove from dev group
uv remove --group dev pytest

# Or just remove the group entirely
# Edit pyproject.toml and remove the [project.optional-dependencies] section
```

### Cleanup Operations

```bash
# Remove unused packages (advanced)
# Check what's not imported in your code
# Then manually uv remove them

# uv doesn't have auto-cleanup like some tools
# But you can:
pip show  # List all
# Then uv remove each unnecessary one
```

## Advanced Dependency Management

### Handling Conflicts

**Scenario:** Two packages need incompatible versions of a dependency.

```toml
# Your dependencies
dependencies = [
    "package-a>=1.0",  # Requires numpy==1.24
    "package-b>=2.0",  # Requires numpy==1.25
]

# uv resolution error:
# "Packages conflict: numpy 1.24 vs 1.25"
```

**Solution:**

```bash
# Option 1: Relax one constraint
uv add "package-b>=2.0,<3.0"

# Option 2: Use pre-release versions
uv add --pre package-b

# Option 3: Investigate upstream fixes
# Check if newer versions of either package fix it
uv add --upgrade
```

### Platform-Specific Dependencies

Some packages are only needed on certain platforms:

```toml
[project]
dependencies = [
    "requests>=2.28",
    'pywin32>=300; sys_platform == "win32"',  # Windows only
    'python-daemon>=2.3; sys_platform == "linux"',  # Linux only
]
```

Use in uv:

```bash
# uv handles automatically
uv sync  # Only installs relevant packages

# On Windows: pywin32 installed
# On Linux: python-daemon installed
# Both: Only on their respective platforms
```

### Python Version-Specific Dependencies

```toml
[project]
requires-python = ">=3.8"
dependencies = [
    "typing-extensions>=4.0; python_version < '3.9'",
]

[project.optional-dependencies]
asyncio_backport = [
    'asyncio-contextmanager; python_version < "3.10"',
]
```

### Private Package Registries

For internal/private packages:

```bash
# Configure in command
uv add private-package --index-url https://private.registry/simple/

# Or configure in pyproject.toml
# See Configuration section
```

### Dependency Extras

Some packages have optional features:

```bash
# Install with extras
uv add "sqlalchemy[postgresql]"
uv add "requests[security]"
uv add "django[postgres,redis]"

# Your pyproject.toml shows:
dependencies = [
    "sqlalchemy[postgresql]>=2.0",
]
```

## Examining Dependencies

### View Installed Packages

```bash
# List packages in current environment
uv run pip list

# Output:
# Package       Version
# ------------- -------
# pip           23.0
# requests      2.31.0
# urllib3       2.0.0
```

### Dependency Tree

```bash
# See dependency relationships
uv run pip show requests

# Name: requests
# Version: 2.31.0
# Summary: Python HTTP for Humans.
# Home-page: https://requests.readthedocs.io
# Author: Kenneth Reitz
# License: Apache 2.0
# Requires: charset-normalizer, idna, urllib3, certifi
# Required-by:
```

### Detailed Dependency Analysis

```bash
# Use pipdeptree (install first)
uv add pipdeptree
uv run pipdeptree

# Output shows hierarchy:
# requests==2.31.0
#   ├── certifi [required: >=2017.4.17, installed: 2023.7.22]
#   ├── charset-normalizer [required: >=2, <4, installed: 3.3.2]
#   ├── idna [required: >=2.5,<4, installed: 3.4]
#   └── urllib3 [required: >=1.21.1,<3, installed: 2.0.7]
```

## Syncing Environments

### Initial Sync (Fresh Install)

```bash
# Install all dependencies from lock file
uv sync

# Creates or updates .venv/
# Installs exact versions from uv.lock
# Removes packages not in lock file
```

### Keeping Environment in Sync

```bash
# After pulling changes with new dependencies
git pull origin main
uv sync

# Environment now matches lock file exactly
```

### Syncing with Specific Groups

```bash
# Sync without dev dependencies (production)
uv sync --no-group dev

# Sync only dev dependencies
uv sync --no-group default --group dev

# Sync multiple groups
uv sync --group dev --group docs
```

## Best Practices

### Version Pinning Strategy

**Development:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",     # Allow newer versions
    "black>=23.0",
]
```

**Production:**
```toml
[project]
dependencies = [
    "django~=4.2",     # Allow patch updates only
    "psycopg2-binary~=2.9",
]
```

**Critical:**
```toml
dependencies = [
    "cryptography==41.0.4",  # Exact version for security
]
```

### Dependency Review Checklist

```bash
# Before adding a dependency, ask:

# 1. Is it necessary?
#    Can standard library solve this?

# 2. Is it maintained?
uv run pip show package_name | grep -i "author"

# 3. How many dependencies does it add?
uv run pipdeptree -p package_name | wc -l

# 4. License compatible?
#    Check package metadata

# 5. Security issues?
#    Check security databases
```

## Troubleshooting

### Issue: "Resolver failed - no compatible version"

```bash
# Error: "Could not find a version that satisfies..."

# Solution 1: Check constraints
cat pyproject.toml | grep dependencies

# Solution 2: Relax constraints
uv add "package>=1.0"  # Instead of "package==1.0"

# Solution 3: Check Python version
uv python list
# Package might not support your Python version
```

### Issue: "Dependency conflicts"

```bash
# Error: "Packages conflict..."

# Solution 1: Check requirements
uv run pip show package_name

# Solution 2: Find common version
uv lock --upgrade

# Solution 3: Use different packages
# Replace conflicting package with alternative
```

### Issue: "Lock file out of sync"

```bash
# Error: "pyproject.toml and uv.lock don't match"

# Solution: Regenerate lock file
rm uv.lock
uv lock

# Or
uv lock --refresh
```

## Common Workflows

### Starting a Web Project

```bash
uv init web_api
cd web_api

# Add core dependencies
uv add fastapi uvicorn sqlalchemy

# Add dev tools
uv add --group dev pytest pytest-asyncio httpx

# View result
cat pyproject.toml
```

### Data Science Project

```bash
uv init data_project
cd data_project

# Data processing
uv add pandas numpy scipy

# ML
uv add scikit-learn xgboost

# Viz
uv add matplotlib seaborn plotly

# Notebooks
uv add jupyter ipython

# Dev tools
uv add --group dev pytest black mypy
```

### Converting from requirements.txt

```bash
# Legacy way (don't do this with uv)
# pip install -r requirements.txt

# uv way
# For each line in requirements.txt:
uv add package1
uv add package2
# ... etc

# Or automate:
# while read line; do uv add "$line"; done < requirements.txt
```

## Next Steps

- **Lock files deep dive:** See [Virtual Environments](05_virtual_envs.md)
- **Run your code:** Jump to [Scripts & Tools](06_scripts_and_tools.md)
- **Production setup:** Read [Best Practices](08_best_practices.md)

---

**Pro Tip:** Always commit `uv.lock` to version control. This ensures everyone (and CI/CD) uses the exact same environment. 📦

