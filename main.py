from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import AsyncSessionLocal
from models import Item

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/items/")
async def create_item(
    name: str,
    description: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    item = Item(name=name, description=description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@app.get("/items/")
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()
