from sqlalchemy import Table,MetaData,Column,Integer,String,ForeignKey
from db import engine
#user
metadata=MetaData()
#user Table
user=Table(
    "users",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String(length=50),nullable=False),
    Column("email",String,nullable=False),
    Column("phone",Integer,nullable=False)
)
# #table for relationship
post=Table(
    "post",
    metadata,
    Column("id",Integer,primary_key=True),
    #column showing relation b/w user and post Table(one to many)
    Column("user_id",Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
    Column("title",String,nullable=False),
    Column("content",String,nullable=False)
   
 )
def create_table():
    metadata.create_all(engine)