from fastapi import FastAPI,Depends
from typing import Annotated
app=FastAPI()
class common:
    def __init__(self,q:str|None=None,skip:int=0,limit:int=100):
        self.q=q
        self.skip=skip
        self.limit=limit
#using dependecise
@app.get("/item")
async def read_item(commons:Annotated[common,Depends(common)]):
    return commons
@app.get("/user")
async def user(common_user:Annotated[common,Depends()]):
    return common_user

