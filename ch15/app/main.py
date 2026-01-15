from fastapi import FastAPI,Header,Body
from typing import Annotated
from pydantic import BaseModel,Field
app=FastAPI()
# Header with a Pydantic Model
# class ProductHeader(BaseModel):
    
#     author: strYHKL
#     accept_lan:str|None= Field( default=None)
#     tracking_id: list[str]=[]
# @app.get("/pro")
# async def get_item(header:Annotated[ProductHeader,Header()]):
#     return {
#         "header":header
#     }

# # C:\>curl -X GET ^
# More? -H "accept:application/json" ^

# More? -H "author:anu" ^
# More? -H "accept-lan:eng" ^
# More? -H "tracking_id:hello123" ^
# More? -H "tracking_id:hello456" ^
# More? -H "extra_id:123" ^
# More? http://127.0.0.1:8000/pro
# {"header":{"author":"anu","accept_lan":"eng","tracking_id":["hello123","hello456"]}}
# forbidding extra Header
class ProductHeader(BaseModel):
    model_config={
        "extra":"forbid"
    }
    author: str
    accept_lan:str|None= Field( default=None)
    tracking_id: list[str]=[]
@app.get("/pro")
async def get_item(header:Annotated[ProductHeader,Header()]):
    return {
        "header":header
    }
