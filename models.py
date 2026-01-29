from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)
