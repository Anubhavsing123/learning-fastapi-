from fastapi import FastAPI
from app.user.model import User
from app.product.model import Prodcut
from app.db.config import create_tables
from contextlib import asynccontextmanager
@asynccontextmanager
async def life(app:FastAPI):
    create_tables()
    yield
app=FastAPI(lifespan=life)

