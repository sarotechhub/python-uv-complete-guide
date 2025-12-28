# Installing uv – Get Up and Running

This guide covers installing uv on Windows, macOS, and Linux, plus verification and troubleshooting.

## System Requirements

Before installation, ensure you have:

- **Operating System:** Windows 10+, macOS 10.12+, or Linux
- **Python:** Python 3.8 or later (for running projects)
- **Internet:** Connection required for downloading packages
- **Disk Space:** ~100 MB for uv and caches
- **Permissions:** User-level installation (no sudo required)

## Installation Methods

### Method 1: Official Installer (Recommended)

The official installation script is the easiest and most reliable method.

#### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This command:
1. Downloads the installer script
2. Detects your OS and architecture
3. Downloads the appropriate binary
4. Installs to `~/.local/bin/uv`
5. Adds to your PATH

**What happens next:**

```bash
# The installer will print instructions
# Follow them to add uv to your PATH

# Option 1: If you use bash (add to ~/.bashrc or ~/.bash_profile)
export PATH="$HOME/.local/bin:$PATH"

# Option 2: If you use zsh (add to ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Option 3: If you use fish (add to ~/.config/fish/config.fish)
set -gx PATH $HOME/.local/bin $PATH

# Restart your shell or source the profile
source ~/.bashrc
# or
source ~/.zshrc
```

#### Windows

**Using PowerShell (Recommended):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**What happens:**
1. Script detects Windows version and architecture
2. Downloads uv binary
3. Installs to `%APPDATA%\Python\Scripts` or Program Files
4. Automatically adds to PATH

**If PowerShell fails:**

```powershell
# Allow PowerShell scripts for this session
Set-ExecutionPolicy -ExecutionPolicy ByPass -Scope Process
# Then run the installer
irm https://astral.sh/uv/install.ps1 | iex
```

### Method 2: Using Package Managers

#### Homebrew (macOS)

```bash
brew install uv
```

Benefits:
- Seamless integration with macOS
- Auto-updates with `brew upgrade uv`
- Removes with `brew uninstall uv`

#### Winget (Windows)

```powershell
winget install astral-sh.uv
```

Benefits:
- Native Windows package manager
- Easy uninstall and updates
- System-wide availability

#### APT (Debian/Ubuntu)

```bash
# Add repository
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or install from source/direct download
```

#### DNF (Fedora/RHEL)

```bash
dnf install uv
```

### Method 3: From Source

For development or custom builds:

```bash
git clone https://github.com/astral-sh/uv.git
cd uv
cargo build --release
./target/release/uv --version
```

### Method 4: Manual Download

Download pre-compiled binaries from [GitHub Releases](https://github.com/astral-sh/uv/releases):

```bash
# Linux/macOS: Download appropriate binary
# Windows: Download .exe or .msi

# Make executable (Linux/macOS)
chmod +x ./uv

# Move to PATH
sudo mv ./uv /usr/local/bin/
# Or Windows: Add to a folder in PATH
```

## Verification

After installation, verify uv is working:

```bash
# Check version
uv --version
# Output: uv 0.1.15 (or newer)

# Check installation location
uv --version --verbose
# Shows: /path/to/uv binary location

# Quick functionality test
uv help
# Shows all available commands
```

### Detailed Verification

```bash
# Verify installation details
uv version

# Check Python detection
uv python list
# Shows: Available Python interpreters

# Test basic operation
uv pip list  # If you have a project's venv
```

## Configuration After Installation

### 1. Set Python Preference (Optional)

uv auto-detects Python, but you can configure preferences:

```bash
# View available Python versions
uv python list

# Set default Python version
# uv will use this by default in new projects
export UV_PYTHON_PREFERENCE=3.11
```

### 2. Configure Index (Advanced)

By default, uv uses PyPI. To use a custom index:

```bash
# Create ~/.uv/uv.toml
[tool.uv.index]
url = "https://pypi.org/simple/"

# Or for private index
url = "https://your-private-registry.com/simple/"
```

### 3. Set Cache Directory (Optional)

```bash
# By default: ~/.cache/uv (Linux/macOS) or %APPDATA%\uv (Windows)

# Custom cache location
export UV_CACHE_DIR=/custom/cache/path  # Linux/macOS
# or
setx UV_CACHE_DIR C:\custom\cache\path  # Windows
```

### 4. Enable Python Downloads (Optional)

uv can download Python versions automatically:

```bash
# Enable in ~/.uv/uv.toml
allow-python-downloads = true

# Or via environment variable
export UV_PYTHON_DOWNLOADS=allow
```

## Troubleshooting Installation

### Issue 1: "Command not found: uv"

**Symptom:** After installation, `uv --version` returns command not found.

**Solution 1: Restart terminal**
```bash
# Close and reopen your terminal/shell
# The PATH wasn't updated in the current session
```

**Solution 2: Manually add to PATH**

Linux/macOS:
```bash
# Find where uv installed
which uv  # If it exists somewhere else
# Or check ~/.local/bin/uv

# Add to shell profile
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Windows PowerShell:
```powershell
# Check if in PATH
where.exe uv

# If not found, add manually
$env:Path -split ';' | where { $_ -like '*AppData*' }
# Ensure %APPDATA%\Python\Scripts is in PATH
```

### Issue 2: "Permission denied" (Linux/macOS)

```bash
# Fix permissions
chmod +x ~/.local/bin/uv

# Or reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue 3: Windows PowerShell Execution Policy Error

```powershell
# Error: "cannot be loaded because running scripts is disabled"

# Solution 1: Bypass for this session
powershell -ExecutionPolicy ByPass -Command `
  "irm https://astral.sh/uv/install.ps1 | iex"

# Solution 2: Change policy permanently (requires admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Network/Download Failures

```bash
# Error: "Failed to download binary"

# Solution 1: Check internet connection
ping www.github.com

# Solution 2: Manual download and install
# Visit: https://github.com/astral-sh/uv/releases
# Download appropriate binary for your OS
# Extract and add to PATH manually

# Solution 3: Install via package manager
# macOS: brew install uv
# Windows: winget install astral-sh.uv
```

### Issue 5: "Python not found"

```bash
# Error: "Could not find Python installation"

# Solution 1: Verify Python installed
python --version
python3 --version

# Solution 2: Update PATH if Python moved
# uv should find Python automatically

# Solution 3: Explicitly set Python path
export UV_PYTHON=/path/to/python  # Linux/macOS
setx UV_PYTHON C:\Python\python.exe  # Windows
```

### Issue 6: Proxy/Corporate Network Issues

If behind a corporate proxy:

```bash
# Set proxy for downloads
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# Or configure in ~/.uv/uv.toml
[tool.uv]
index-url = "https://your-internal-registry.com/simple/"
```

## Upgrading uv

### From Official Installer

```bash
# Re-run installation script
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

### From Package Manager

```bash
# Homebrew (macOS)
brew upgrade uv

# Winget (Windows)
winget upgrade astral-sh.uv

# APT (Linux)
apt update && apt upgrade uv
```

## Uninstalling uv

### Official Installation

```bash
# Linux/macOS
rm ~/.local/bin/uv

# Windows (via PowerShell)
Remove-Item -Path "$env:APPDATA\Python\Scripts\uv.exe"
```

### Package Manager

```bash
# Homebrew
brew uninstall uv

# Winget
winget uninstall astral-sh.uv

# APT
apt uninstall uv
```

## Verifying Installation Success

Here's a complete verification checklist:

```bash
# 1. Version check
uv --version  # Should show version number

# 2. Help command
uv help  # Should show command list

# 3. Python detection
uv python list  # Should show available Pythons

# 4. Create test project
uv init test_project
cd test_project

# 5. Add a package
uv add requests

# 6. Run Python
uv run python -c "import requests; print(requests.__version__)"

# 7. Verify lock file
ls uv.lock  # or dir uv.lock on Windows

# Clean up
cd ..
rm -rf test_project  # or rmdir /s test_project on Windows
```

If all these steps succeed, uv is correctly installed! ✅

## Next Steps

Now that uv is installed:

1. **Quick Start:** Jump to [Project Setup](03_project_setup.md)
2. **Understand Basics:** Read [Virtual Environments](05_virtual_envs.md)
3. **Start Using:** See [Dependency Management](04_dependency_management.md)

## Getting Help

If you encounter issues:

1. **Official Docs:** https://docs.astral.sh/uv/
2. **GitHub Issues:** https://github.com/astral-sh/uv/issues
3. **Discussions:** https://github.com/astral-sh/uv/discussions

---

**Pro Tip:** Keep uv updated to get the latest features and bug fixes. Check for updates monthly!

