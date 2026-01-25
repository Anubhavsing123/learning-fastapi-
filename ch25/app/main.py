from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse

app=FastAPI()
name={
    "apple":"REd light color",
    "grapes":"green  in color"
}
# create Exceptions
class Excep(Exception):
    def __init__(self,name:str):
        self.name=name
#custom exceptions
@app.exception_handler(Excep)
async def main(res:Request,exc:Excep):
    return  JSONResponse(
        status_code=404,
        content={"msg":f"{exc.name} is not valid name" },


    )
@app.get("/{fruit}")
async def fruits(fruit:str):
    if fruit not in name:
        raise Excep(name=fruit)
    return name[fruit]

