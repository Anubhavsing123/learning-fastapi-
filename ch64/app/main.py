from fastapi import FastAPI,Depends
from typing import Annotated
app=FastAPI()

#sync depends function
def get_user():
    return {"ok ":"this is the user list"}
#async depens function
async def get_product():
    return {"ok":"this is the product list"}
#creating depends as aliasing function
@app.get("/user")
async def get_user(sync:Annotated[dict,Depends(get_user)],asyn:Annotated[dict,Depends(get_product)]):

    return {"sync":sync,"asyn":asyn}


