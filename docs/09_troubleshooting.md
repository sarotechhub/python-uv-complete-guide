# Troubleshooting & FAQs

Common issues, solutions, and frequently asked questions about uv.

## Frequently Asked Questions (FAQs)

### General Questions

#### Q: Is uv production-ready?
**A:** Yes! uv is actively used in production by numerous companies. Key maturity indicators:
- ✅ Stable API (semantic versioning)
- ✅ Comprehensive test suite
- ✅ Active maintenance by Astral
- ✅ Growing community adoption
- ⚠️ Some features still in development (workspaces)

**Recommendation:** Safe for production use in 2024+

---

#### Q: Can I use uv with my existing project?
**A:** Absolutely! uv is backward compatible:

```bash
# Existing project with requirements.txt
uv init .  # Initialize uv

# Existing project with pyproject.toml
uv init .  # Use existing config

# Existing project with Poetry
uv init .  # Read Poetry's pyproject.toml
```

---

#### Q: Do I need to learn new commands?

**A:** Minimal learning curve:

```
Concept          pip         Poetry        uv
─────────────────────────────────────────────
Add dependency   pip install poetry add     uv add
Remove           pip uninstall poetry remove uv remove
Install all      pip install  poetry install uv sync
Lock             pip-tools    poetry lock   uv lock
Run script       python       poetry run    uv run
```

If you know any of these, you'll pick up uv quickly.

---

#### Q: Will uv replace my entire workflow?
**A:** Yes, for most teams:

```
Old workflow:
├─ venv (environment)
├─ pip (install)
├─ requirements.txt (lock?)
└─ Multiple tools

uv workflow:
└─ uv (everything)
```

One tool handles all package and environment management.

---

#### Q: What about Anaconda/Miniconda users?
**A:** uv works well for pure Python projects:

```bash
# If you use Conda for:
├─ NumPy/SciPy/compiled packages → Keep Conda
├─ System libraries → Keep Conda
└─ Pure Python → Switch to uv ✓

# uv doesn't handle:
├─ System package management
├─ C/Rust extension compilation
└─ Non-Python dependencies
```

For data science, consider both:
```bash
# Use Conda for scientific stack
conda create -n myenv python=3.11 numpy pandas

# Use uv for pure Python within that env
uv init .  # Works inside conda env
```

---

### Installation Questions

#### Q: Installation fails on Windows
**A:** Common Windows issues:

```powershell
# Issue 1: PowerShell execution policy
# Solution:
powershell -ExecutionPolicy ByPass -Command `
  "irm https://astral.sh/uv/install.ps1 | iex"

# Issue 2: Network/proxy issues
# Solution 1: Use Winget
winget install astral-sh.uv

# Solution 2: Manual download
# Download from https://github.com/astral-sh/uv/releases
# Extract and add to PATH
```

---

#### Q: How do I uninstall uv?
**A:** Depends on installation method:

```bash
# Official installer (macOS/Linux)
rm ~/.local/bin/uv

# Official installer (Windows)
# Settings → Apps → uv → Uninstall
# Or delete from AppData\Python\Scripts\

# Homebrew (macOS)
brew uninstall uv

# Winget (Windows)
winget uninstall astral-sh.uv
```

---

#### Q: Can I install uv in a virtual environment?
**A:** Not recommended. uv should be installed system-wide:

```bash
# ❌ Don't do this
python -m venv env
source env/bin/activate
pip install uv  # uv manages envs, shouldn't be in one

# ✅ Install globally
curl -LsSf https://astral.sh/uv/install.sh | sh

# Then use uv to manage project envs
uv init my_project
```

---

### Dependency Issues

#### Q: I'm getting "resolver conflict" errors
**A:** When dependencies are incompatible:

```bash
# Error: "Packages conflict: requests 2.31 vs 2.30"

# Solution 1: Understand why
# Check which packages need which version
uv tree --package requests

# Solution 2: Relax constraints if possible
uv add "requests>=2.30"

# Solution 3: Use different package
# If two packages need incompatible versions
# Look for alternatives or wait for updates

# Solution 4: Check for pre-releases
uv add --pre package_name
```

---

#### Q: What's the difference between sync and install?
**A:** Simple answer:

```
uv sync   = Sync environment to match lock file (destructive)
           = Remove packages not in lock file
           = Ensures exact reproducibility
           = Preferred for production

uv pip install = Traditional pip install (non-destructive)
           = Add to environment, don't remove others
           = Use if you must mix with other tools
           = Avoid if possible
```

**Recommendation:** Use `uv sync` always.

---

#### Q: Can I have different versions for different projects?
**A:** Yes! Each project is isolated:

```bash
# Project A uses requests 2.31
cd project_a
uv add "requests==2.31.0"
uv run python -c "import requests; print(requests.__version__)"
# 2.31.0

# Project B uses requests 2.30
cd ../project_b
uv add "requests==2.30.0"
uv run python -c "import requests; print(requests.__version__)"
# 2.30.0

# Each project's .venv/ is completely isolated
```

---

### Virtual Environment Questions

#### Q: Where does uv create virtual environments?
**A:** By default, in project root:

```
my_project/
├── .venv/           # ← Created here

# Location: .venv/ or venv/ in project root
# uv auto-detects these locations

# Custom location (rarely needed)
uv venv ~/myenvs/my_project
# Then edit pyproject.toml if needed
```

---

#### Q: Can I use multiple .venv directories?
**A:** Not directly, but workaround:

```bash
# Create project structure
mkdir -p projects/project_a
mkdir -p projects/project_b

# Each has isolated .venv
cd projects/project_a && uv init .
cd projects/project_b && uv init .

# Each runs in own environment
uv run python script.py
```

---

#### Q: Do I need to activate .venv manually?
**A:** No! uv does it automatically:

```bash
# ✅ Right way (automatic)
uv run python script.py
uv run pytest
uv run black src/

# ❌ Old way (manual, unnecessary)
source .venv/bin/activate
python script.py
deactivate

# Manual activation only needed for:
# - Interactive shell with specific environment
# - Shell scripts that need venv Python
```

---

### Lock File Questions

#### Q: Why commit uv.lock to git?
**A:** Ensures reproducibility:

```
Without uv.lock:
├─ Developer A: uv sync → numpy 1.24
├─ Developer B: uv sync → numpy 1.25 ← Different!
├─ CI/CD: uv sync → numpy 1.26 ← Different!
└─ Production: Different again!

With uv.lock:
├─ Developer A: uv sync → numpy 1.24 ✓
├─ Developer B: uv sync → numpy 1.24 ✓
├─ CI/CD: uv sync → numpy 1.24 ✓
└─ Production: numpy 1.24 ✓
```

**Answer:** Without lock file, builds are non-deterministic.

---

#### Q: How often should I update lock file?
**A:** Depends on your needs:

```bash
# Weekly (modern approach)
uv lock --upgrade
# Check if updates work
uv run pytest
# Commit if tests pass

# Monthly (balanced)
uv lock --upgrade
# Review for breaking changes
# Merge to main if stable

# Per-dependency (controlled)
uv add --upgrade package_name
# Granular control over upgrades
```

---

#### Q: What if lock file is corrupted?
**A:** Regenerate it:

```bash
# Delete corrupted lock file
rm uv.lock

# Regenerate
uv lock

# Or force regeneration
uv lock --refresh
```

---

### Python Version Questions

#### Q: How do I use different Python versions?
**A:** Via `.python-version` file:

```bash
# Create project with specific version
uv init --python 3.11 my_project

# Or change existing
echo "3.10" > .python-version

# Next command uses that version
uv run python --version
# Python 3.10.x

# View available
uv python list
```

---

#### Q: Can uv download Python automatically?
**A:** Yes, enable it:

```toml
# In pyproject.toml or .uv/uv.toml
[tool.uv]
python-downloads = "automatic"  # or "allow"
```

Or via environment:
```bash
export UV_PYTHON_DOWNLOADS=allow
```

Then:
```bash
echo "3.12.0" > .python-version
uv run python --version
# uv downloads and installs Python 3.12.0 automatically
```

---

#### Q: What Python versions does uv support?
**A:** Currently:

```
Minimum: Python 3.8
Latest supported: Python 3.13 (beta)

Tested and stable: 3.8, 3.9, 3.10, 3.11, 3.12
```

---

### Performance Questions

#### Q: Why is my first `uv sync` slow?
**A:** First sync downloads packages:

```
First sync:
├─ Resolve dependencies
├─ Download packages (network-bound)
└─ Install to .venv
⏱️ Time: 10-30 seconds

Subsequent syncs:
├─ Use cached packages
└─ Install from cache
⏱️ Time: 1-3 seconds
```

Subsequent runs are fast due to caching.

---

#### Q: How do I speed up CI/CD?
**A:** Use layer caching:

```dockerfile
# Docker example
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy only lock file (layer caching)
COPY pyproject.toml uv.lock ./

# Install deps (cached if lock file unchanged)
RUN uv sync --frozen --no-dev

# Copy source code
COPY src ./src

# Run application
CMD ["uv", "run", "python", "-m", "myapp"]
```

Cache benefits:
- ✅ First build: Full download (slow)
- ✅ Subsequent builds: Reuse cached layer if lock file unchanged
- ✅ Significant CI/CD speedup

---

### Workflow Questions

#### Q: How do I work with monorepos?
**A:** Each package gets own environment:

```
monorepo/
├── packages/
│   ├── core_lib/
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   └── src/
│   ├── web_app/
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   └── src/
│   └── api/
│       ├── pyproject.toml
│       ├── uv.lock
│       └── src/
└── root_pyproject.toml  # Optional: workspace config

# Work on individual package
cd packages/core_lib
uv sync

# Or root-level sync (when workspace is ready)
uv sync -r  # Sync all packages
```

---

#### Q: Can I use uv with existing pip requirements.txt?
**A:** Yes, migration path:

```bash
# Existing requirements.txt
cat requirements.txt
# flask==2.3.0
# sqlalchemy==2.0.0
# requests>=2.28.0

# Create uv project
uv init .

# Read requirements and add them
while read req; do 
  uv add "$req" 
done < requirements.txt

# Verify
uv sync
python -c "import flask; print(flask.__version__)"

# Delete old files
rm requirements.txt
git add pyproject.toml uv.lock
```

---

#### Q: How do I handle pre-release packages?
**A:** Control with flags:

```bash
# Allow pre-releases
uv add --pre package_name

# In pyproject.toml
[tool.uv]
prerelease = "allow"  # allow, if-necessary, disallow

# Specific pre-release
uv add "package>=2.0b1"
```

---

## Common Error Messages and Solutions

### Error: "Python not found"

```
❌ Error: "Could not find Python installation"

Causes:
1. Python not installed
2. Python not in PATH
3. Specified Python version not available

Solutions:

Option 1: Install Python
# Linux/macOS
brew install python@3.11

# Windows
# Download from https://www.python.org
# Or use uv's built-in downloader
uv python install 3.11

Option 2: Check PATH
which python3  # Linux/macOS
where python  # Windows

Option 3: Check .python-version
cat .python-version
# If version is unavailable
uv python install 3.11
echo "3.11" > .python-version
```

---

### Error: "No compatible version found"

```
❌ Error: "Could not find a version that satisfies all requirements"

Cause: Version constraints conflict

Solution:

# Check constraint
uv add --dry-run "package>=1.0,<1.5"

# Relax if needed
uv add "package>=1.0"  # Allow any 1.x
# Or check if newer fixes it
uv add "package"  # Latest

# Last resort: Different package
# If no compatible version exists
# Look for alternative package
```

---

### Error: "Lock file conflict"

```
❌ Error: "uv.lock and pyproject.toml don't match"

Cause: Manual edits to pyproject.toml without updating lock file

Solution:

# Regenerate lock file
uv lock

# Or
uv lock --refresh

# Then verify
uv sync
```

---

### Error: "Permission denied"

```
❌ Error: "Permission denied" (Linux/macOS)

Cause: uv binary not executable

Solution:

chmod +x ~/.local/bin/uv

# Or reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### Error: "Module not found"

```
❌ Error: "ModuleNotFoundError: No module named 'package'"

Causes:
1. Package not in lock file
2. Environment not activated
3. Wrong Python version

Solutions:

# Check if installed
uv run pip list | grep package

# Install if missing
uv add package

# Verify right environment
uv run python -c "import sys; print(sys.prefix)"
# Should show .venv directory

# Check Python version
uv run python --version
```

---

### Error: "Platform-specific issue"

```
❌ Error: Package won't install on your platform

Example: Windows-only package on Linux

Solution:

# Check supported platforms
uv add --dry-run package

# Use platform-specific marker
# In pyproject.toml
dependencies = [
    'pywin32; sys_platform == "win32"',
    'fcntl; sys_platform != "win32"',
]

# uv installs only relevant packages
```

---

## Debugging Tips

### Enable Verbose Output

```bash
# More detail in error messages
uv --verbose add package

# Very verbose (debugging)
uv --verbose --verbose add package
```

### Check Environment Details

```bash
# See what uv sees
uv python list  # Available Pythons
uv pip list     # Installed packages
uv run env      # Environment variables (Linux/macOS)
uv run set      # Environment variables (Windows)
```

### Verify Installation

```bash
# Test uv itself
uv --version
uv help

# Test with simple project
uv init test_project
cd test_project
uv add requests
uv run python -c "import requests; print(requests.__version__)"
rm -rf ../test_project  # Cleanup
```

## Reporting Issues

If you find a bug or have an issue:

### Check Existing Issues
```
https://github.com/astral-sh/uv/issues
```

### Create New Issue
Include:
1. **OS and version** (Windows 11, macOS 14, Ubuntu 22.04)
2. **uv version** (`uv --version`)
3. **Python version** (`python --version`)
4. **Error message** (full output)
5. **Steps to reproduce** (minimal example)
6. **Expected behavior** (what should happen)

### Example Issue Report
```
### Environment
- OS: Windows 11
- uv: 0.1.15
- Python: 3.11.4
- Behind proxy: Yes

### Description
`uv add requests` fails with timeout

### Error
```
Connection timeout: failed to download ...
```

### Steps to Reproduce
1. Create new project: `uv init test`
2. Try to add: `uv add requests`
3. Fails after 30 seconds

### Expected
Package should install successfully
```

## Getting Help

### Official Resources
- **Docs:** https://docs.astral.sh/uv/
- **GitHub:** https://github.com/astral-sh/uv
- **Discussions:** https://github.com/astral-sh/uv/discussions
- **Discord:** (if available)

### Community
- Stack Overflow (tag: `python-uv`)
- Reddit: r/learnprogramming, r/Python
- Twitter: @astral_sh

### Professional Support
For enterprise support, check:
- Astral website: https://astral.sh
- Enterprise services may be available

## Quick Reference

```bash
# Project creation
uv init my_project              # New project
uv init --python 3.11 proj      # Specific Python
uv init --package proj          # Package layout

# Dependencies
uv add package                  # Add dependency
uv add --group dev pytest       # Dev dependency
uv remove package               # Remove
uv add --upgrade                # Update one
uv lock --upgrade               # Update all

# Environment
uv sync                         # Create/sync env
uv venv                         # Create venv
source .venv/bin/activate       # Manual activation (rare)

# Running
uv run python script.py         # Run script
uv run pytest                   # Run tests
uv run black src/               # Run tool

# Maintenance
uv lock                         # Lock file
uv lock --refresh               # Force refresh
rm -rf .venv && uv sync         # Rebuild env
```

---

**Still stuck?** Create an issue on GitHub or ask the community! The uv team and community are responsive and helpful. 🤝

