from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import List
app=FastAPI()
# # Nested  body Models
#submodel
# class Cat(BaseModel):
#     name:str=Field(title="Catergory name",
#                    description=" the name of the product",
#                    max_length=50,
#                    min_length=1)
#     description: str| None=Field(default=None,title="category description",
#                                  description="Catergory description",
#                                  max_length=100
#                                  )
# #Model wich will use 
# class Product(BaseModel):

#     name: str = Field(
#         title="Product Name",
#         description="Describing about the product",
#         max_length=100,
#         min_length=3,
#         pattern="^[A-Za-z0-9 ]+$"
#     )

#     price: float = Field(
#         gt=0,
#         title="Product Price",
#         description="The price of the product in USD, must be greater than 0"
#     )

#     stock: int | None = Field(
#         default=None,
#         ge=0,
#         title="No of product",
#         description="The number of products available"
#     )
#     cat:Cat |None=Field(default=None,
#                         title="Product Cat.",
#                         description="the ca. belong to ")
# @app.post("/product")
# async def creat_item(product:Product):
#     return product

#attribute with list  of submodel
class Cat(BaseModel):
    name:str=Field(title="Catergory name",
                   description=" the name of the product",
                   max_length=50,
                   min_length=1)
    description: str| None=Field(default=None,title="category description",
                                 description="Catergory description",
                                 max_length=100
                                 )
#Model wich will use 
class Product(BaseModel):

    name: str = Field(
        title="Product Name",
        description="Describing about the product",
        max_length=100,
        min_length=3,
        pattern="^[A-Za-z0-9 ]+$"
    )

    price: float = Field(
        gt=0,
        title="Product Price",
        description="The price of the product in USD, must be greater than 0"
    )

    stock: int | None = Field(
        default=None,
        ge=0,
        title="No of product",
        description="The number of products available"
    )
    cat:List[Cat] |None=Field(default=None,
                        title="Product Cat.",
                        description="the ca. belong to ")
@app.post("/product")
async def creat_item(product:Product):
    return product
