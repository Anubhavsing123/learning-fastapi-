from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import init_db
from app.account.router import router as r1
@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app=FastAPI(lifespan=lifespan,title="Prosql",description="this is prosql db")
app.include_router(r1)