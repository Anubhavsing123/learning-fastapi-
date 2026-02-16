from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,Float
class Product(Base):
    __tablename__="products"
    stock_id:Mapped[int]=mapped_column(Integer,primary_key=True,nullable=False)
    stock_price:Mapped[float]=mapped_column(Float,nullable=False)
    no_stock:Mapped[int]=mapped_column(Integer,nullable=True)
    def __rep__(self):
        return f"<prodcut id={self.stock_id} price={self.stock_price} "