from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer
#user model 
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(length=25),nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    phone:Mapped[int]=mapped_column(Integer,nullable=False)
    def __rep__(self)->str:
        return f"<User id={self.id} name={self.name} email={self.email}"
        