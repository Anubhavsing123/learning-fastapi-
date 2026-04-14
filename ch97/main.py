from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_table
from app.account.router import router as r1
@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_table()
    yield
app=FastAPI(lifespan=lifespan,title="Prosql",description="this is prosql db")
app.include_router(r1)