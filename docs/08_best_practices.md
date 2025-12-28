# Best Practices for Production Use

Production-grade patterns, workflows, and strategies for reliable Python applications.

## Project Structure

### Recommended Layout (Standard Library Style)

```
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_utils.py
│   └── fixtures/
├── docs/
│   ├── index.md
│   ├── api.md
│   └── getting_started.md
├── scripts/
│   ├── migrate_data.py
│   ├── cleanup.py
│   └── seed_db.py
├── pyproject.toml
├── README.md
├── .gitignore
├── .python-version
└── Makefile

# src/ layout advantages:
# ✅ Tests import from installed package
# ✅ Forces proper package structure
# ✅ Prevents sys.path hacks
# ✅ Matches production installation
```

### Complete pyproject.toml Example

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my_project"
version = "0.1.0"
description = "Production-ready application"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Dev Team", email = "dev@company.com"}
]
license = {text = "MIT"}
keywords = ["api", "data", "tool"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/myorg/my_project"
Documentation = "https://my_project.readthedocs.io"
Repository = "https://github.com/myorg/my_project.git"
Issues = "https://github.com/myorg/my_project/issues"

[project.dependencies]
requests = ">=2.31.0,<3"
pydantic = ">=2.0,<3"
pydantic-settings = ">=2.0,<3"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
    "pytest-asyncio>=0.21.0",
]
docs = [
    "sphinx>=6.0",
    "sphinx-rtd-theme>=1.2",
    "sphinx-autodoc-typehints>=1.23",
]
perf = [
    "uvloop>=0.17.0",
    "orjson>=3.9.0",
]

[project.scripts]
my-app = "my_project.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

[tool.black]
line-length = 100
target-version = ["py38"]
include = '\.pyi?$'

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP"]
ignore = ["E501"]  # Black handles line length
target-version = "py38"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.isort]
profile = "black"
line_length = 100

[tool.uv]
managed = true
```

## Dependency Management Patterns

### Version Pinning Strategy

**Production Dependencies:**

Use **compatible release** for stability:

```toml
[project.dependencies]
# Allow patch-level updates only
django = "~=4.2.0"          # >= 4.2.0, < 4.3.0
celery = "~=5.3.0"          # >= 5.3.0, < 5.4.0
redis = "~=4.5.0"           # >= 4.5.0, < 4.6.0
psycopg2-binary = "~=2.9.0" # >= 2.9.0, < 2.10.0
```

**Why:**
- ✅ Receives bug fixes and security patches
- ✅ Won't break with breaking changes
- ✅ Minimal maintenance
- ✅ Predictable behavior

**Critical/Security Dependencies:**

Pin exact versions:

```toml
[project.dependencies]
# Security-critical, don't auto-update
cryptography = "==41.0.4"
pydantic-core = "==2.10.1"
```

**Why:**
- ✅ Stability for security packages
- ✅ Explicit version changes
- ✅ Traceable in security audits

**Development Dependencies:**

Use flexible versions:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
```

**Why:**
- ✅ Developers always get latest tools
- ✅ Consistent formatting/linting
- ✅ No version management overhead

### Dependency Review Checklist

Before adding production dependencies:

```python
# Checklist
📋 1. Necessity
    □ Can standard library solve this?
    □ Is it a core feature?
    □ Worth the maintenance?

📋 2. Maintenance
    □ Is it actively maintained?
    □ Release frequency: >= 1x/year?
    □ Community size: Active discussions?

📋 3. Dependencies
    □ How many transitive deps? (< 10 ideal)
    □ Are those maintained too?
    □ License compatible?

📋 4. Security
    □ Any known vulnerabilities? (check CVE)
    □ Responsible disclosure process?
    □ Does it need frequent updates?

📋 5. Performance
    □ Size impact? (> 10MB concerning)
    □ Startup overhead?
    □ Runtime performance?

📋 6. License
    □ Compatible with project license?
    □ Commercial usage allowed?
    □ Patent/trademark issues?
```

### Vulnerability Scanning

```bash
# Install safety
uv add --group dev safety

# Scan for vulnerabilities
uv run safety check

# Check specific packages
uv run safety check requests pandas
```

## Testing and Quality

### Comprehensive Test Setup

```bash
# Create test project
uv init my_project

# Add testing framework
uv add --group dev pytest pytest-cov

# Add quality tools
uv add --group dev black ruff mypy

# Create tests/
mkdir tests
```

### Test Organization

```
tests/
├── __init__.py
├── unit/
│   ├── test_core.py
│   ├── test_utils.py
│   └── test_models.py
├── integration/
│   ├── test_database.py
│   ├── test_api.py
│   └── test_external.py
├── fixtures/
│   ├── __init__.py
│   ├── db_fixtures.py
│   └── api_fixtures.py
└── conftest.py  # Shared fixtures

# Run specific tests
uv run pytest tests/unit/test_core.py

# Run by marker
uv run pytest -m unit
uv run pytest -m integration

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### CI/CD Configuration (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]

    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: uv sync --group dev
      
      - name: Lint with Ruff
        run: uv run ruff check src/
      
      - name: Format check with Black
        run: uv run black --check src/
      
      - name: Type check with mypy
        run: uv run mypy src/
      
      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY . .

# Create virtual environment and install
RUN uv sync --no-dev

# Run application
CMD ["uv", "run", "python", "-m", "my_project"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=0
      - DATABASE_URL=postgresql://...
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
```

## Deployment Strategies

### Local Development

```bash
# Install with dev dependencies
uv sync

# Run with reload (development)
uv run uvicorn main:app --reload

# Or with make
make dev
```

### Staging Environment

```bash
# Minimal dependencies only
uv sync --no-group dev

# Run without reload (production-like)
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# With process manager
uv run gunicorn main:app -w 4 --bind 0.0.0.0:8000
```

### Production Environment

```bash
# Only runtime dependencies
uv sync --no-dev

# Run with production settings
uv run gunicorn main:app \
  -w 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info

# Or with other ASGI servers
uv run uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: myregistry/my-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: DEBUG
          value: "0"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Security Best Practices

### Secure Configuration

```python
# src/my_project/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    secret_key: str  # From environment
    database_url: str  # From environment
    
    class Config:
        env_file = ".env"  # Local development only
        env_file_encoding = "utf-8"

settings = Settings()
```

```bash
# .env (development only, never commit)
DEBUG=True
SECRET_KEY=dev-key-never-use-in-production
DATABASE_URL=sqlite:///./test.db
```

```bash
# .gitignore
.env
.env.local
*.key
*.pem
```

### Dependency Security

```bash
# Regular vulnerability checks
uv run safety check --json > security_report.json

# Automated checks in CI
safety check --fail-on-vulnerability

# Keep dependencies updated
uv lock --upgrade  # Monthly
```

### Secret Management

```python
# Never hardcode secrets
❌ DATABASE_URL = "postgres://user:password@host/db"

# Use environment variables
✅ DATABASE_URL = os.getenv("DATABASE_URL")

# Or secure vaults
✅ from vault import get_secret
   DATABASE_URL = get_secret("database_url")
```

## Performance Optimization

### Production-Grade Optimizations

```toml
[project.optional-dependencies]
perf = [
    "uvloop>=0.17.0",      # Fast event loop
    "orjson>=3.9.0",       # Fast JSON encoding
    "httpx[http2]>=0.24.0",  # HTTP/2 support
]
```

```python
# src/my_project/app.py (FastAPI example)
from fastapi import FastAPI
import uvloop
import asyncio

# Use uvloop for faster async
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()

# Use orjson for faster JSON
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

@app.get("/")
async def root():
    return ORJSONResponse({"message": "Fast response"})
```

### Caching

```python
# Dependency caching
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_data(param: str) -> dict:
    # Computed once, cached for same params
    return compute_something(param)

# HTTP caching headers
from fastapi import Response

@app.get("/data")
async def get_data():
    return Response(
        content="...",
        headers={"Cache-Control": "max-age=3600"}
    )
```

## Monitoring and Observability

### Structured Logging

```toml
[project.dependencies]
python-json-logger = ">=2.0.0"
```

```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure JSON logging
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
# Output: {"user_id": 123, "ip": "192.168.1.1", "message": "User logged in"}
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers"""
    return {
        "status": "ok",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.get("/health/ready")
async def readiness_check():
    """Check if service is ready to handle traffic"""
    try:
        # Check database
        await db.execute("SELECT 1")
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}, 503
```

## Documentation

### API Documentation

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="My API",
    description="Production-ready API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# OpenAPI/Swagger automatically generated
```

### Code Documentation

```python
def process_data(data: dict[str, str]) -> list[int]:
    """
    Process input data and return results.
    
    Args:
        data: Dictionary with keys 'values' containing space-separated integers
        
    Returns:
        List of processed integers
        
    Raises:
        ValueError: If input format is invalid
        
    Example:
        >>> process_data({"values": "1 2 3"})
        [2, 4, 6]
    """
    try:
        values = map(int, data["values"].split())
        return [v * 2 for v in values]
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid input: {e}")
```

## Common Patterns

### Makefile for Common Tasks

```makefile
.PHONY: help install dev lint format test clean run docker

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | awk '{print $$1}' | sed 's/:$//'

install:
	uv sync

dev:
	uv run uvicorn main:app --reload

lint:
	uv run ruff check src/
	uv run mypy src/

format:
	uv run black src/
	uv run ruff check --fix src/

test:
	uv run pytest --cov=src

clean:
	rm -rf .venv/ dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	uv run python -m my_project

docker:
	docker build -t my-app:latest .
	docker run -p 8000:8000 my-app:latest
```

## Checklist for Production Readiness

```
📋 Code Quality
  ✅ Type hints throughout codebase
  ✅ Comprehensive test coverage (>80%)
  ✅ Linting and formatting (ruff, black)
  ✅ No warnings in mypy

📋 Dependencies
  ✅ All dependencies pinned in pyproject.toml
  ✅ uv.lock committed to version control
  ✅ No security vulnerabilities (safety check)
  ✅ License compliance verified

📋 Documentation
  ✅ README with setup instructions
  ✅ API documentation (OpenAPI/Swagger)
  ✅ Architecture documentation
  ✅ Deployment guide

📋 Testing
  ✅ Unit tests passing
  ✅ Integration tests passing
  ✅ CI/CD pipeline green
  ✅ Coverage reports good

📋 Deployment
  ✅ Docker image tested
  ✅ Environment variables documented
  ✅ Health checks implemented
  ✅ Logging configured

📋 Monitoring
  ✅ Structured logging enabled
  ✅ Error tracking configured
  ✅ Performance metrics tracked
  ✅ Alerting rules defined

📋 Security
  ✅ No hardcoded secrets
  ✅ HTTPS/TLS configured
  ✅ Input validation implemented
  ✅ CORS configured appropriately
```

## Next Steps

- **Troubleshoot issues:** See [Troubleshooting & FAQs](09_troubleshooting.md)
- **Review performance:** Check [Performance Comparison](07_performance_comparison.md)

---

**Key Principle:** A production-ready project uses uv to manage dependencies consistently across development, testing, staging, and production environments. 🚀

