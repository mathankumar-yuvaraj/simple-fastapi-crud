from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

# Example table
items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),  # new field included
)
