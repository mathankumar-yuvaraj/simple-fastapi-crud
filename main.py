from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database
from models import items, metadata
from sqlalchemy import create_engine

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None

# Startup: connect and create tables automatically
@app.on_event("startup")
async def startup():
    await database.connect()
    # Create tables if they don't exist
    engine = create_engine(str(database.url))
    metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# CRUD endpoints
@app.post("/items/")
async def create_item(item: Item):
    query = items.insert().values(
        name=item.name,
        description=item.description
    )
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}

@app.get("/items/")
async def read_items():
    query = items.select()
    return await database.fetch_all(query)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    query = items.update().where(items.c.id == item_id).values(
        name=item.name,
        description=item.description
    )
    await database.execute(query)
    return {**item.dict(), "id": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {"message": "Item deleted"}
