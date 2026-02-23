from fastapi import FastAPI
from app.user.model import User
from app.product.model import Prodcut
from app.db.config import create_tables
from contextlib import asynccontextmanager
from app.user.service import *
@asynccontextmanager
async def life(app:FastAPI):
    create_tables()
    yield
app=FastAPI(lifespan=life)
@app.post("/post")
def new_user(new_user:dict):
    user=create_user(name=new_user["name"],email=new_user["email"])
    return user
@app.get("/users")
def get_all():
    user=get_all_user()
    return user



