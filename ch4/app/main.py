#query pararmeter
from fastapi import FastAPI,Query
from typing import List
app=FastAPI()
#single query parameter
# @app.get("/item")
# async def main1(category:str):
#     return {"status":"OK","category":category}
#optional query parameter
# @app.get("/items/")
# def get_items(limit:int=10):
#     return {"limit":limit}
#multiple query parameter
# @app.get("/items/")
# async def get_items(limit:int=10,skip:int=0):
#     return {"limit":limit,"skip":skip}
#boolean Query parameter
# @app.get("items/")
# async def get_item(active:bool=True):
#     return {"active":active}
#list Query Parameter
@app.get("/items/{year}")
async def get_items(year:str,tags:List[str]=Query([])):
    return {"tags":tags}





