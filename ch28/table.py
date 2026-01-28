from  db import engine
from sqlalchemy import MetaData,Table,Column,Integer,String,ForeignKey
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
    Column("user_id",Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    Column("title",String,nullable=False),
    Column("content",String,nullable=False)
   
)
#table for relationship one to one
profile=Table(
    "profile",
    metadata,
    Column("id",Integer,primary_key=True),
    #column showing relation b/w user and profile Table(one to one) and unique only for this
    Column("user_id",Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,unique=True)
    Column("bio",String,nullable=False),
    Column("address",String,nullable=False)
   
)
#many to many
address=Table(
    "address",
    metadata,
     Column("id",Integer,primary_key=True),
   
    Column("adderss",String,nullable=False),
    Column("country",String,nullable=False)
)
#raw will be unqiue and we are using Sqlalchemy
user_adderss=Table(
    "user_address",
    metadata,
     #column showing relation b/w user and user_address Table(one to one) and unique only for this
    Column("user_id",Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False),
     #column showing relation b/w user_address and addresst Table(many to many) and unique only for this
    Column("id",Integer,ForeignKey("address.id",ondelete="CASCADE"),nullable=False),


)
#create table
def create_table():
    metadata.create_all(engine)
