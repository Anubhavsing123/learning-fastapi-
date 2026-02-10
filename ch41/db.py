from sqlalchemy.ext.asyncio import create_async_engine
DB_URL = "sqlite+aiosqlite:///sqlite.db"
engine = create_async_engine(DB_URL, echo=True)


