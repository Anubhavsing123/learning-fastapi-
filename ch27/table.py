from db import engine
from sqlalchemy import MetaData,Table,Column,Integer,String
metadata=MetaData()
#user Table
user=Table(
    "user",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String(length=50),nullable=False),
    Column("email",String,nullable=False,unique=True),
    Column("phone",Integer,nullable=False,unique=True)




)
#create table in database
def create_table():
    metadata.create_all(engine)
#drop table in database
def drop_table():
    metadata.drop_all(engine)

