from fastapi import FastAPI
from app.service import service
from pydantic import BaseModel
app=FastAPI()
class User(BaseModel):
    name:str
    email:str
    phone:int
    
@app.post("/create")
def user(user:User):
    service.create_user(name=user.name,email=user.email,mobile=user.phone)
    return {"status":"ok"}
@app.get("/")
def get_all():
    user=service.get_all()
    return user
