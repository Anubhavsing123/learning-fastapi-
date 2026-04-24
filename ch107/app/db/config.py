from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (AsyncAttrs,create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession

)
from fastapi import Depends
from typing import Annotated,AsyncGenerator
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path=os.path.join(BASE_DIR,"sqlite.db")
DATABASE_URL=f"sqlite+aiosqlite:///{db_path}"
engine=create_async_engine(DATABASE_URL,echo=True,future=True)
async_session=async_sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
class Base(AsyncAttrs,DeclarativeBase):
    pass
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Table Created...")
async def create_session():
     async with async_session() as sess:
         yield sess
SessionDep=Annotated[AsyncSession,Depends(create_session)]
