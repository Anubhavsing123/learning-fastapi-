from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
app=FastAPI()
class Product (BaseModel):
    id:int
    name: str
    price:float
    stock: int |None=None
class ProductOut(BaseModel):
    name:str
    price:float
#without respone model
# @app.get("/item")
# async def  get_product():
#     return {"name ":"anu"}
# with responde model
# @app.get('/item',response_model=ProductOut)
# async def  get_product():
#     return {"name":"anu","price":34.444}

# @app.post('/item',response_model=ProductOut)
# async def  get_product(product:Product):
#     return product
class UserBase(BaseModel):
    full_name:str
    last_name:str
class UserIn(UserBase):
    passw:str
@app.post('/item',)
async def  get_product(user:UserIn)->UserBase:
    return user
