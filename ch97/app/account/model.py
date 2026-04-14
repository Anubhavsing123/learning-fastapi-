from app.db.config import Base
from sqlalchemy import String,Integer
from sqlalchemy.orm import Mapped,mapped_column
class User(Base):
    __tablename__="user"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(20),nullable=False)
    email:Mapped[str]=mapped_column(String(50),nullable=False,unique=True)
