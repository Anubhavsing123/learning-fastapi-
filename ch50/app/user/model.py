from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer
from app.db.Base import Base
#user model
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(length=50),nullable=False)
    email:Mapped[str]=mapped_column(String(length=50),nullable=False,unique=True)
    def __repr__(self)->str:
        return f"user id={self.id} name={self.name} email={self.email}"
    
