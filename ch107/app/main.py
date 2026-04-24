from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.product.router import router as r1
@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    yield
app=FastAPI(lifespan=lifespan,title="Product")
app.include_router(r1)