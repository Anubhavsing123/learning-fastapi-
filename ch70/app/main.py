from fastapi import FastAPI,HTTPException,Depends
from typing import Annotated
app=FastAPI()
#Dependecies with yield
class OwnerError(Exception):
    pass

def get_user():
    try:
        yield "Raj"
    except OwnerError as e:
        raise HTTPException(status_code=404,detail=f"owner error:{e}")
@app.get("/item/{id}")
def get_item(id:str,username:Annotated[str,Depends(get_user)]):
        data = {
    "pressure-cooker":
        {"description": "Essential for making dal-chawal",
         "owner": "Priya"},
    "scooty":
        {"description": "Zippy ride for city streets",
         "owner": "Raj"},
}
        if id not in data:
            raise HTTPException(status_code=404,detail="id not found")
        item=data[id]
        if item["owner"]!=username:
            raise OwnerError(username)
        return item
