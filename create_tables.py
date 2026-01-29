# create_tables.py
import asyncio
from database import engine, Base

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



asyncio.run(main())
