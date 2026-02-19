from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,Float
from app.db.Base import Base
#product model
class Product(Base):
    __tablename__="products"
    stock_id:Mapped[int]=mapped_column(Integer,primary_key=True)
    stock_price:Mapped[float]=mapped_column(Float,nullable=False)
    number_of_stock:Mapped[int]=mapped_column(Integer,nullable=False)
    def __rep__ (self)->str:
        return f"<Product id={self.stock_id} stock_price={self.stock_price} number_of_stock={self.number_of_stock}"
