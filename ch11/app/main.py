from fastapi import FastAPI
from pydantic import BaseModel,Field
app=FastAPI()
## m-1 using Field level example in Pydantic body  example value
# class Product(BaseModel):
#     name:str=Field(examples=["Moto G"])
#     price:float=Field(examples=[23.56])
#     stock: int| None=Field(default =None,examples=[43])
# @app.post("/product")
# async def creat_item(product:Product):
#     return product
# m-2 usign pydantic's json_scheama_extra
class Product(BaseModel):
    name:str
    price:float
    stock: int | None=None
    model_config={
       "json_schema_extra":{
           "example":[
               {
                   "name":"Moto E",
                   "price":34.56,
                   "stock":10
               }
           ]
       }
    }
@app.post("/product")
async def creat_item(product:Product):
    return product