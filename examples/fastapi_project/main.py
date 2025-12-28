from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Example API", version="0.1.0")


class Item(BaseModel):
    """Item model for request/response."""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


# In-memory database
items_db = {}


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the Example API"}


@app.get("/items/")
def list_items():
    """List all items."""
    return {"items": list(items_db.values())}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items/")
def create_item(item: Item):
    """Create a new item."""
    items_db[item.id] = item
    return {"created": item}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {"updated": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = items_db.pop(item_id)
    return {"deleted": deleted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
