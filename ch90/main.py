from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_table
from app.account.model import *
from app.account.router import router as r1
@asynccontextmanager
async def lifespan(app=FastAPI):
    create_table()
    yield
app=FastAPI(lifespan=lifespan)
app.include_router(r1)