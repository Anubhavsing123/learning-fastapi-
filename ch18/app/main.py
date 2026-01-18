from fastapi import FastAPI
from pydantic import BaseModel
from typing import List,Annotated,Any,Optional
app=FastAPI()

product_db={
    "1":{
        "id":"1",
        "name":"laptop",
        "price":34.4,
        "stock":20,
         "is_active":True
    },
    "2":{
        "id":"2",
        "name":"Mobile",
        "price":34.4,
        "stock":20,
        "is_active":True
    },
    "3":{
        "id":"3",
        "name":"Fan",
        "price":34.4,
        "stock":20,"is_active":True
    }
}
class Product(BaseModel):
    id:str
    name:str
    price:float
    stock :int
    desprtion: Optional[str]=None
    tax: float=20.45 #default value
    #exclude the uset defalut value
# @app.get("/item/{product}",response_model=Product,response_model_exclude_unset=True)
# async def  get_product(product_id:str):
#     return product_db.get(product_id,{})
# #include sepecific field
# @app.get("/item/{product_id}",response_model=Product,response_model_include={"name","price"})
# async def get_product(product_id:str):
#     return product_db.get(product_id,{})
# exclude Specific field
@app.get("/item/{product_id}",response_model=Product,response_model_exclude={"name","price"})
async def get_product(product_id:str):
    return product_db.get(product_id,{})
