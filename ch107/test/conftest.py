import pytest 
import pytest_asyncio
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (create_async_engine,AsyncSession,
                                    async_sessionmaker

)
from sqlalchemy import text
from app.main import app
from app.db.config import Base,create_session
from typing import AsyncGenerator
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path=os.path.join(BASE_DIR,"test_sqlite.db")
DATABASE_URL=f"sqlite+aiosqlite:///{db_path}"
engine=create_async_engine(DATABASE_URL,echo=True,future=True)
test_async_session=async_sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
#override the gcreate_session dependency to use the test database.
async def override_get_session()->AsyncGenerator[AsyncSession,None]:
    async with test_async_session() as test_session:
        yield test_session
app.dependency_overrides[create_session]=override_get_session
#Initialize FastAPI TestClient for testing endpoints .
client=TestClient(app)
@pytest_asyncio.fixture(scope="function")
async def setup_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)#drop_all means drop all the tables
        await conn.run_sync(Base.metadata.create_all)# create the tables
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)#drop all the tables after test
    await engine.dispose() # close the database connection
    if os.path.exists(db_path):
        for _ in range(5): # retry up to 5 time windows file locking
            try:
                os.remove(db_path)
                break
            except PermissionError:
                import time
                time.sleep(0.5)
@pytest_asyncio.fixture
async def test_session(setup_data)->AsyncGenerator[AsyncSession,None]:
    async with test_async_session() as session:
        await session.execute(text("DELETE FROM product"))
        await session.commit()
        yield session
@pytest_asyncio.fixture
def test_client():
    return client

