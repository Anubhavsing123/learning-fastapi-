from app.service.service import create_user,get_all
from app.product.service import create_product,get_all_pro
from fastapi import FastAPI
from pydantic import BaseModel
from app.db.config import engine
from app.db.Base import Base

class User_validation(BaseModel):
    name:str
    email:str
class Product_val(BaseModel):
    price:float
    number:int


app=FastAPI()


@app.post('/user')
async def user_create(user:User_validation):
    await create_user(nam=user.name,email=user.email)
    return {"stauts":"ok"}
@app.get("/get")
async def get_all_user():
    user=await get_all()
    return user
#product
@app.post("/product")
async def create_pro(prod:Product_val):
     produ=await create_product(stock_price=prod.price,number_of_stock=prod.number)
     return produ
@app.get("/")
async def get_all():
    prod=await get_all_pro()
    return prod