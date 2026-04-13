from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends 
from typing import Annotated,AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncAttrs
import ssl
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = (
    "mysql+aiomysql://3JhVCTrvZyvscet.root:nm4RezBH1FPGyF8S@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test")
ssl_ctx = ssl.create_default_context()

engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "ssl": ssl_ctx
    },
    echo=True,
)


#load enviroment variable from.env file

async_session=async_sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
class Base(AsyncAttrs,DeclarativeBase):
    pass
async def create_Table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Table...")
async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session
SessionDep=Annotated[AsyncSession,Depends(get_session)]