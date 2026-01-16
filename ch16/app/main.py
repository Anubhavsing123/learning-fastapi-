from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
# class Product(BaseModel):
#     name: str
#     price: float
#     stock: int |None=None

# without return type

# @app.get("/product")
# async def get_product():
#     return {"status":"OK"}
# with return type
# @app.get("/product")
# async def get_product()->Product:
#     return {"id": 2,"price":34.55,"stock":12}
# class Productout(BaseModel):
#     name: str
#     price:float
# @app.post("/")
# async def  main(product:Product)->Productout:
#     return product
class UserBase(BaseModel):
    username: str
    full_name:str |None=None
class UserIn(UserBase):
    password:str
@app.post("/")
async def  create_user(user:UserIn)->UserBase:
    return user
