from db import engine
from sqlalchemy import Integer,String,Table,Column,MetaData
metadata=MetaData()
#user sql core
user=Table(
    "users",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String,nullable=False),
    Column("email", String(length=50), nullable=False),
    Column("phone", String(length=10), nullable=False, unique=True)

)
