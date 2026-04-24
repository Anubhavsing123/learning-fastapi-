from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,Integer,Float
from app.db.config import Base
class Product(Base):
    __tablename__="product"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)

    title:Mapped[str]=mapped_column(String,nullable=False)
    price:Mapped[float]=mapped_column(Float,nullable=False)
    stock:Mapped[float]=mapped_column(Float,nullable=False)
