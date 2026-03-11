from fastapi import FastAPI,Depends
from typing import Annotated
app=FastAPI()
#creating depence function
async def common_parameter(q: str |None=None,skip :int=0,limit:int=100):
    return {"q":q,"skip":skip,"limit":limit}

# using dependencies
# @app.get("/use")
# async def read(comms: Annotated[dict, Depends(common_parameter)]):
#     return comms
#creating type aslias 
CommonDep=Annotated[dict,Depends(common_parameter)]
@app.get("/use")
async def read(comms:CommonDep):
    return comms


