from fastapi import FastAPI,Header,HTTPException,Depends
from typing import Annotated

async def verify(token:Annotated[str,Header()]):
    if token!="my_sceret_token":
        raise HTTPException(status_code=404,detail="Not found")
#using dependecise
app=FastAPI(dependencies=[Depends(verify)])
@app.get("/item")
async def read_item():
    return {"ok":"items"}
@app.get("/user")
async def user():
    return {"ok ":"user"}

