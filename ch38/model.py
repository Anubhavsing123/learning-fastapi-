from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,Table,Integer,Column
from db import engine
#model/table file
class Base(DeclarativeBase):
    pass
#user model/table
class User(Base):
    __tablename__="user"
    #editor know id is int throught by Mapped but mapped_column for db
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50),nullable=True)
    email:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    phone :Mapped[int]=mapped_column(Integer,nullable=False)
    add:Mapped[str]=mapped_column(String)
    def __repr__(self)->str:
        return f"<user(id={self.id},name={self.name},email={self.email})>"


def create_table():
  Base.metadata.create_all(engine)
