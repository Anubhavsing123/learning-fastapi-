from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
##create or insert data without pydantic model
# @app.post('/product')
# async def create_product(new_product:dict):
#     return new_product
#with Pydantic
class Product(BaseModel):
    id:int
    name:str
    price:float
    stock: int | None=None
# @app.post('/product')
# async def create_product(new_product:Product):
#     print(new_product.id)
#     print(new_product.name)
#     print(new_product.price)
#     print(new_product.stock)
#     return new_product
#add new calculated atrribute
@app.post('/product')
async def create_product(new_product:Product):
    product_dict=new_product.model_dump()
    price_with_tax=new_product.price +(new_product.price*18/100)
    product_dict.update({"price_tax":price_with_tax})
    return product_dict
#combine path paramete with request body
# @app.put("/product/{product_id}")
# async def product_id(product_id:int,new_product:Product):
#     return {"Product_id":product_id,"new_product":new_product}
#combine request body with path and query parameter
# @app.put("/product/{product_id}")
# async def product_id(product_id:int,new_product:Product,dis:float| None=None):
#     print(dis)
#     return {"Product_id":product_id,"new_product":new_product,"discount":dis}
    
# @app.get("/product/{product_id}")
# async def product_get_id(product_id:int,dis:float| None=None):
#     print(dis)
#     return {
#         "Product_id": product_id,
#         "discount": dis
#     }
    