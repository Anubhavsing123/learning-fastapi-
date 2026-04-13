from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_Table
from app.account.router import router as r1
@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_Table()
    yield
app=FastAPI(lifespan=lifespan)
app.include_router(r1)
