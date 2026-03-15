from fastapi import FastAPI,Header,HTTPException,Depends
from typing import Annotated
app=FastAPI()
#dependcies in the path operation
async def verify(token:Annotated[str,Header()]):
    if token!="my_sceret_token":
        raise HTTPException(status_code=404,detail="Not found")
@app.get("/user",dependencies=[Depends(verify)])
async def read_item():
    return {"ok":"data is correct"}