from sqlmodel import Session,select

from app.product.model import *
async def create_product(session:Session,new_product:Product)->ProductOut:
    product=Product(title=new_product.title,description=new_product.description)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product    
async def get_all_product(session:Session)->list[ProductOut]:
    stmt=select(Product)
    product=session.exec(stmt)
    return product.all()
async def get_product_id(session:Session,new_id:int)->ProductOut:
    stmt=select(Product).where(Product.id==new_id)
    product=session.exec(stmt).first()
    return product
async def delete_product(session:Session,new_id:int,):
    stmt=select(Product).where(Product.id==new_id)
    pro=session.exec(stmt).first()
    if pro is  None:
        return {"msg": "Product not found"}
    session.delete(pro)
    session.commit()
    return {"msg":pro}


