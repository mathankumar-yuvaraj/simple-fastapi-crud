from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database
from models import items

app = FastAPI()

class Item(BaseModel):
    name: str

# Connect to DB on startup
@app.on_event("startup")
async def startup():
    await database.connect()
    # Create tables if not exist (optional)
    from sqlalchemy import create_engine
    from models import metadata
    engine = create_engine(str(database.url))
    metadata.create_all(engine)

# Disconnect on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Create
@app.post("/items/")
async def create_item(item: Item):
    query = items.insert().values(name=item.name)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}

# Read all
@app.get("/items/")
async def read_items():
    query = items.select()
    return await database.fetch_all(query)

# Read one
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    query = items.update().where(items.c.id == item_id).values(name=item.name)
    await database.execute(query)
    return {**item.dict(), "id": item_id}

# Delete
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {"message": "Item deleted"}
