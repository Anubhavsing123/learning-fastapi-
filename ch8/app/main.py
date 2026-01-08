from fastapi import FastAPI,Body
from pydantic import BaseModel
from typing import Annotated
app=FastAPI()
#Mulitple Body Parameter
class Product(BaseModel):
    name:str
    price:float
    stock: int |None=None
class Seller(BaseModel):
    username:str
    full_name:str | None=None
# @app.post("/product")
# async def create_item(product:Product,seller:Optional[Seller]=None):
#     return {"product":product,"seller":seller}
#single value in body
# @app.post("/product")
# async def create_item(product:Product, seller:Seller,
#                       sec_key : Annotated[str,Body()]):
#     print("Body",Body)
#     return {"product":product,"seller":seller,"sec_key":sec_key}
#without embedd 
# @app.post("/product")
# async def create_item(product:Product, 
#                       ):
#     print("Body",Body)
#     return {"product":product}
#with embeded
@app.post("/product")
async def create_item(product:Annotated[Product,Body(embed=True)], 
                      ):
    print("Body",Body)
    return {"product":product}

