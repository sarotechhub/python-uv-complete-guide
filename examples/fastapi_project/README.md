# FastAPI Project Example

A complete FastAPI web application demonstrating REST API development with uv.

## Features

- FastAPI web framework
- Pydantic models for validation
- CRUD operations example
- Async support
- Comprehensive tests with pytest
- Development server with uvicorn

## Getting Started

### Install dependencies

```bash
uv sync
```

### Run the development server

```bash
uv run python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Run tests

```bash
uv run pytest
uv run pytest -v
uv run pytest --cov
```

### Format and lint code

```bash
uv run black .
uv run ruff check .
uv run ruff check . --fix
```

## Project Structure

```
fastapi_project/
├── pyproject.toml      # Project configuration
├── main.py             # FastAPI application
├── test_main.py        # Unit tests
└── README.md          # This file
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/items/` | List all items |
| GET | `/items/{item_id}` | Get specific item |
| POST | `/items/` | Create new item |
| PUT | `/items/{item_id}` | Update item |
| DELETE | `/items/{item_id}` | Delete item |

## Example Usage

```bash
# List items
curl http://localhost:8000/items/

# Create an item
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Laptop", "price": 999.99}'

# Get specific item
curl http://localhost:8000/items/1

# Update item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Updated Laptop", "price": 899.99}'

# Delete item
curl -X DELETE http://localhost:8000/items/1
```

## Next Steps

- Add database integration (SQLAlchemy)
- Implement authentication (JWT)
- Add database migrations (Alembic)
- Deploy with Docker
