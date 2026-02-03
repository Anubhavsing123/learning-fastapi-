from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String
from db import engine
class Base(DeclarativeBase):
    pass
#user model/table
class userTable(Base):
    __tablename__="user"
    #editor know id is int throught by Mapped but mapped_column for db
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50),nullable=True)
    email:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    phone:Mapped[int]=mapped_column(nullable=False,unique=True)
   
    def __rep__(self)->str:
        return f"<user(id={self.id},name={self.name},email={self.email})>"
class Address(Base):
     id:Mapped[int]=mapped_column(primary_key=True)
     street:Mapped[int]=mapped_column(String(50),nullable=True)
     country:Mapped[str]=mapped_column(String,nullable=False,unique=True)
     dist :Mapped[str]=mapped_column(String,nullable=False,unique=True)
     def __rep__(self)->str:
        return f"<Address(id={self.id!r},street={self.street!r})>"

#create table
def create_table():
  Base.metadata.create_all(engine)
#drop table
def drop_table():
    Base.metadata.drop_all(engine)