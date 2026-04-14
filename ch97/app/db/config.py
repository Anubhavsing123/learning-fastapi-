from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated,AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncAttrs
from fastapi import Depends
from decouple import config
DB_URL=config('DATABASE_URL')
engine=create_async_engine(DB_URL,echo=True,future=True)
async_session=async_sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)

class Base(AsyncAttrs,DeclarativeBase):
    pass
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Table......")
async def get_session()->AsyncGenerator[AsyncAttrs,None]:
    async with async_session() as session:
        yield session
SessionDep=Annotated[AsyncSession,Depends(get_session)]

