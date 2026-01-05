from fastapi import FastAPI,status,Query
from typing import Annotated,List
from pydantic import AfterValidator

products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "High performance", "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest model", "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 49.99, "category": "Appliances"},
]
app=FastAPI()
# @app.get("/item",status_code=status.HTTP_202_ACCEPTED)
# def main():
#      return products_db
#  query parameter validation
# @app.get("/product")
# async def  prodcut(se:str |None=None):
#     if se:
#         ser = se.lower()
#         fill = []
#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)
#         return fill
#     return products_db
#valdiation without anonated
# @app.get("/product")
# async def  prodcut(se:str |None=Query(default=None,max_length=5)):
#     if se:
#         ser = se.lower()
#         fill = []
#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)
#         return fill
#     return products_db
#valdiation with anonated
# @app.get("/product")
# async def  prodcut(se:Annotated[str |None,Query(max_length=5)]=None):
#     if se:
#         ser = se.lower()
#         fill = []
#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)
#         return fill
#     return products_db

#valdiation with anonated with reg
# @app.get("/product")
# async def  prodcut(se:Annotated[str |None,Query(min_length=5,pattern="^[a-z]+$")]=None):
#     if se:
#         ser = se.lower()
#         fill = []
#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)
#         return fill
#     return products_db
#multiple  search
# @app.get("/product")
# async def  prodcut(se:Annotated[List[str ]|None,Query(max_length=5)]=None):
#     if se:
        
#         fill = []
#         for pro in products_db:
#             for s in se:
#                 if s.lower() in pro["name"].lower():
#                     fill.append(pro)

#         return fill
#     return products_db
# alsia parameter
# @app.get("/product")
# async def  prodcut(se:Annotated[str |None,Query(min_length=5,alias="q")]=None):
#     if se:
#         ser = se.lower()
#         fill = []
#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)
#         return fill
#     return products_db
#adding meta data
@app.get("/product")
# async def product(
#     se: Annotated[
#         str | None,
#         Query(
#             min_length=5,
#             alias="q",
#             title="Search Item",
#             description="About the product detail"
#         )
#     ] = None
# ):
#     if se:
#         ser = se.lower()
#         fill = []

#         for pro in products_db:
#             if ser in pro["name"].lower():
#                 fill.append(pro)

#         return fill

    # return products_db
#deprecating parameter
@app.get("/product")
async def product(
    se: Annotated[
        str | None,
        Query(
            min_length=5,
            alias="q",
            title="Search Item",
            description="About the product detail",
            deprecated=True
        )
    ] = None
):
    if se:
        ser = se.lower()
        fill = []

        for pro in products_db:
            if ser in pro["name"].lower():
                fill.append(pro)

        return fill

    return products_db
#custom validation
def check_vali(id:str):
    if not id.startswith('prod-'):
        raise ValueError('ID must start with "prod-"')
    return id
@app.get('/item')
async def item(id: Annotated[
        str | None,
        AfterValidator(check_vali)
    ] = None):
    if id:
        return {id:"id","msg":"vlid id"}
    return {"msg":"not valid id"}



