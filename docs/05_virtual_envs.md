# Virtual Environments with uv

Deep dive into virtual environment management, the foundation of isolated Python development.

## What are Virtual Environments?

### The Problem They Solve

Without virtual environments, all Python packages go to system Python:

```
/usr/lib/python3.11/site-packages/
├── django==3.2.0     # Project A needs this
├── django==4.2.0     # Project B needs this
└── ...CONFLICT!      # Can only install one version
```

Virtual environments create isolated copies:

```
Project A/.venv/lib/python3.11/site-packages/
├── django==3.2.0 ✓
├── requests==2.25.0
└── ...

Project B/.venv/lib/python3.11/site-packages/
├── django==4.2.0 ✓
├── requests==2.31.0
└── ...

Each project has its own isolated environment!
```

## Virtual Environments with uv

### Automatic Environment Creation

uv creates and manages virtual environments automatically:

```bash
# Create project
uv init my_project
cd my_project

# First uv run command creates .venv automatically
uv run python --version
# .venv/ is created automatically

# Verify it exists
ls -la .venv  # Linux/macOS
dir /a:h .venv  # Windows
```

### What uv Creates

```
my_project/
├── .venv/                    # Virtual environment
│   ├── bin/                  # Linux/macOS executables
│   │   ├── python           # Python interpreter
│   │   ├── pip
│   │   ├── activation script
│   │   └── ...
│   ├── Scripts/              # Windows executables
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── activate.bat
│   ├── lib/                  # Packages
│   │   └── python3.11/site-packages/
│   ├── include/              # C headers (for compilation)
│   └── pyvenv.cfg           # Configuration
├── .python-version           # Python version specification
├── pyproject.toml
└── uv.lock
```

## Creating and Managing Virtual Environments

### Create Virtual Environment Explicitly

```bash
# Create virtual environment in current directory
uv venv

# Creates .venv/ in current directory

# Verify creation
ls .venv/bin/python  # Linux/macOS
dir .venv\Scripts\python.exe  # Windows
```

### Create with Specific Python Version

```bash
# Use Python 3.11
uv venv --python 3.11

# Use specific Python binary
uv venv --python /usr/bin/python3.10

# Use latest Python available
uv venv --python 3
```

### Alternative Location for .venv

```bash
# Create in alternative location
uv venv venv  # Creates venv/ instead of .venv/
uv venv ~/envs/my_project  # Custom path

# Update .venv path in tool configuration if needed
# uv automatically finds .venv/ and venv/ in project root
```

## Activating Virtual Environments

### Automatic Activation (uv's Approach)

**The uv way:** No explicit activation needed!

```bash
# Just run commands with uv
uv run python script.py
uv run pip list
uv run pytest

# uv automatically uses the .venv/
# No manual activation required
```

### Manual Activation

Sometimes you need to activate manually for shell commands:

#### Linux/macOS

```bash
# Activate for current shell session
source .venv/bin/activate

# Shell prompt changes
(my_project) $ echo $VIRTUAL_ENV
/path/to/my_project/.venv

# Now you're in the venv
python --version  # Uses .venv's Python

# Deactivate when done
deactivate
```

#### Windows (PowerShell)

```powershell
# Activate for current session
.venv\Scripts\Activate.ps1

# If PowerShell complains about execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1

# Shell shows activated state
(.venv) PS > $env:VIRTUAL_ENV
C:\path\to\my_project\.venv

# Deactivate
deactivate
```

#### Windows (Command Prompt)

```batch
# Activate
.venv\Scripts\activate.bat

# Shell shows activated state
(my_project) C:\path>

# Deactivate
deactivate.bat
```

### When to Activate Manually

**Rarely needed with uv, but useful for:**

```bash
# Interactive Python shell in venv
source .venv/bin/activate
python  # Interactive interpreter with venv packages

# Running raw pip commands
source .venv/bin/activate
pip install some_package  # Using venv's pip

# Shell scripts using venv Python
source .venv/bin/activate
./my_script.sh  # Uses venv's Python
```

## Environment Isolation

### Verifying Isolation

```bash
# In project 1
cd project_a
uv add requests

# In project 2
cd ../project_b
uv add django

# project_a doesn't have django
uv run python -c "import django" 2>&1
# Error: ModuleNotFoundError

# project_b doesn't have requests
uv run python -c "import requests" 2>&1
# Error: ModuleNotFoundError

# Each environment is completely isolated ✓
```

### Package Installation Locations

```bash
# See where packages install
uv run python -c "import site; print(site.getsitepackages())"

# Output (Linux/macOS):
# ['/path/to/.venv/lib/python3.11/site-packages']

# Compare to system Python:
python3 -c "import site; print(site.getsitepackages())"
# ['/usr/lib/python3.11/site-packages', ...]
```

## Managing Multiple Environments

### Project-Specific Environments

```bash
# Each project gets its own environment
project_a/.venv/        # Project A's packages
project_b/.venv/        # Project B's packages

# Switch between projects
cd project_a
uv run python main_a.py  # Uses project_a/.venv/

cd ../project_b
uv run python main_b.py  # Uses project_b/.venv/
```

### Workspace with Multiple Environments

```
workspace/
├── package_a/
│   ├── .venv/           # A's environment
│   ├── src/
│   └── pyproject.toml
├── package_b/
│   ├── .venv/           # B's environment
│   ├── src/
│   └── pyproject.toml
└── shared/
    ├── common_lib/
    └── ...

# Each package has isolated deps
```

### Development Environment with Multiple Packages

```bash
# Your project depends on internal packages

# pyproject.toml for web_app
[project]
dependencies = [
    "core_package @ file://../core_package",
    "utils_package @ file://../utils_package",
]
```

## Python Version Management

### Specifying Python Version

The `.python-version` file:

```bash
# View current Python version
cat .python-version
# Output: 3.11

# Change to different version
echo "3.10" > .python-version

# Next uv command will use Python 3.10
uv run python --version
# Python 3.10.x
```

### Multiple Python Versions in Project

```bash
# If package supports multiple Python versions
cat pyproject.toml
# requires-python = ">=3.8,<3.12"

# Test with different versions
echo "3.8" > .python-version
uv run pytest tests/

echo "3.11" > .python-version
uv run pytest tests/

# Both work correctly
```

### Automatic Python Download

uv can download Python if not available:

```bash
# Enable in .python-version or command
echo "3.12.0" > .python-version

# uv downloads Python 3.12.0 automatically
uv run python --version

# Check downloaded versions
uv python list
```

## Virtual Environment Caching

### How uv Speeds Things Up

```bash
# First sync takes time
uv sync  # Resolves dependencies, installs

# Subsequent syncs are fast
uv sync  # Reuses cached packages

# Even across projects!
```

### Cache Location

```bash
# macOS/Linux
~/.cache/uv/

# Windows
%LOCALAPPDATA%\uv\Cache\

# View cache
uv cache dir

# Clear cache if needed
rm -rf ~/.cache/uv
```

## Recreating Environments

### Complete Refresh

```bash
# Remove virtual environment
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows

# Recreate from lock file
uv sync

# .venv/ is recreated with exact versions
```

### When to Recreate

**Scenarios:**

1. **Corrupted environment:**
   ```bash
   # If packages are broken
   rm -rf .venv && uv sync
   ```

2. **Upgrade Python:**
   ```bash
   # After updating .python-version
   echo "3.12" > .python-version
   rm -rf .venv && uv sync
   ```

3. **Clean install:**
   ```bash
   # Start fresh
   rm -rf .venv && uv sync
   ```

## Syncing Environments

### Initial Sync

```bash
# First time in a project
uv sync

# Creates .venv/
# Installs all dependencies from uv.lock
```

### Syncing After Changes

```bash
# After someone adds dependencies to pyproject.toml
git pull origin main

# Update your environment
uv sync

# .venv/ now has new packages
```

### Syncing with Groups

```bash
# Include dev dependencies
uv sync --group dev

# Exclude dev dependencies (production)
uv sync --no-group dev

# Multiple groups
uv sync --group dev --group docs
```

## Deactivation and Cleanup

### Deactivating Virtual Environment

```bash
# If you manually activated
source .venv/bin/activate
# do work...
deactivate

# Return to system Python
python --version  # System Python
```

### Removing Virtual Environment

```bash
# Safe to delete (just a directory)
rm -rf .venv

# Recreate when needed
uv sync
```

### Cleanup Best Practices

```bash
# .gitignore should have .venv/
cat .gitignore | grep venv
# Output: .venv/

# Never commit .venv/ to git
# Users will create their own with uv sync

# Commit these instead:
# - pyproject.toml
# - uv.lock
# - .python-version
```

## Troubleshooting Virtual Environments

### Issue: "ModuleNotFoundError: No module named X"

```bash
# Package is in another project's .venv/

# Solution 1: Install in current project
uv add package_name

# Solution 2: Verify you're in correct project
pwd

# Solution 3: Check if environment created
ls -la .venv

# Solution 4: Recreate environment
uv sync
```

### Issue: "Command not found: python"

```bash
# .venv not activated or not found

# Solution 1: Use uv run
uv run python script.py  # Works without activation

# Solution 2: Activate manually
source .venv/bin/activate

# Solution 3: Create environment
uv venv
```

### Issue: "Python version not found"

```bash
# Specified Python version not available

# Solution 1: Check available versions
uv python list

# Solution 2: Install version
uv python install 3.11

# Solution 3: Change .python-version to available version
echo "3.10" > .python-version

# Solution 4: Let uv download it
# In uv.toml set:
allow-python-downloads = true
```

### Issue: "Virtual environment is corrupted"

```bash
# Some package installation failed

# Solution: Recreate
rm -rf .venv
uv sync

# Complete fresh environment installed
```

## Advanced Topics

### Environment with System Packages

```bash
# Rarely needed, but possible
# Use system Python packages + virtual env packages

# Usually not recommended
# Keep environments isolated for reproducibility
```

### Embedding Virtual Environment

```bash
# Docker/CI often embed Python + venv
# But with uv, just install uv + uv.lock = reproducibility
```

### Performance Optimization

```bash
# uv.lock speeds up environment creation
# Commit uv.lock to version control:
git add uv.lock
git commit -m "Update dependencies"

# CI/CD then uses cached lock file
# Builds are 10x faster
```

## Best Practices

### ✅ Do This

```bash
# Use uv run for commands
uv run python script.py

# Commit uv.lock
git add uv.lock

# Use .python-version
echo "3.11" > .python-version

# Sync regularly
uv sync
```

### ❌ Don't Do This

```bash
# Don't manually modify .venv/
# Don't commit .venv/ to git
# Don't use system Python directly
# Don't mix uv and pip without reason
```

## Next Steps

- **Run your code:** See [Scripts & Tools](06_scripts_and_tools.md)
- **Dependency details:** Jump to [Dependency Management](04_dependency_management.md)
- **Production setup:** Read [Best Practices](08_best_practices.md)

---

**Key Insight:** With uv, virtual environments are automatic and transparent. Focus on your code, not environment management! 🚀

