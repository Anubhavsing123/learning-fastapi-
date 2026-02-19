from sqlalchemy import select
from app.db.config import session
from app.product.model import Product
async def create_product(stock_price:float,number_of_stock:int):
    async with session() as sess:
        pro=Product(stock_price=stock_price,number_of_stock=number_of_stock)
        sess.add(pro)
        await sess.commit()
        
        return pro
async def get_all_pro():
    async with session() as sess:
        tmt=select(Product)
        pro=await sess.scalars(tmt)
        return pro.all()

