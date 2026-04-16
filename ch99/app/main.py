from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import Create_tables
from app.account.router import router as r1

@asynccontextmanager
async def lifespan(app:FastAPI):
    await Create_tables()
    yield
app=FastAPI(lifespan=lifespan)
app.include_router(r1)
