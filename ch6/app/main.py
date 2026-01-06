# from fastapi import FastAPI,Path,Query
# from typing import Annotated
# app=FastAPI()
# # path paramter valdiation
# products_db = [
#     {"id": 1, "name": "Laptop", "price": 999.99, "description": "High performance", 
# "category": "Electronics"},
#     {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest model", 
# "category": "Electronics"},
#     {"id": 3, "name": "Coffee Maker", "price": 49.99, "category": "Appliances"},
# ]
# # @app.get("/item/{product_id}")
# # async def get_allproduct (product_id:int):
# #     for pro in products_db:
# #         if pro["id"]==product_id:
# #             return pro
# #         return {"error":"not found"}
# # numerica validation
# # @app.get("/item/{product_id}")
# # async def get_allproduct (product_id:Annotated[int,Path(ge=1,le=3)]):
# #     for pro in products_db:
# #         if pro["id"]==product_id:
# #             return pro
# #     return {"error":"not found"}
# # adding meta data in path paramert
# # @app.get("/item/{product_id}")
# # async def get_allproduct (product_id:Annotated[int,Path(ge=1,le=3,
# #                              title="this is new product line",
# #                               description="this is new product line")]):
# #     for pro in products_db:
# #         if pro["id"]==product_id:
# #             return pro
# #         return {"error":"not found"}
# #combine path and query para
# @app.get("/item/{product_id}")
# async def get_allproduct(
#     product_id: Annotated[
#         int,
#         Path(
#             ge=1,
#             le=3,
#             title="This is product ID",
#             description="Product ID must be between 1 and 3"
#         )
#     ],

#     search_id: Annotated[
#         str | None,
#         Query(
#             min_length=5,
#             alias="q",
#             title="Search Item",
#             description="About the product detail",
#             deprecated=True
#         )
#     ] = None
# ):

#     for pro in products_db:
#         if pro["id"] == product_id:

#             # Query parameter checking
#             if search_id:
#                 if search_id.lower() in pro["name"].lower():
#                     return pro
#                 return {"message": "Search not matched"}

#             return pro

#     return {"error": "Product not found"}
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(
        title="Product ID",
        description="Unique product ID",
        example=101,
        gt=0,
        le=1000
    )
):
    return {"product_id": product_id}