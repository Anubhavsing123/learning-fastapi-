from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#print(BASE_DIR)
db_path=os.path.join(BASE_DIR,"sqlite.db")
DATABASE_URL="sqlite+aiosqlite:///{db_path}"
engine=create_async_engine(DATABASE_URL,echo=True)
session=async_sessionmaker(bind=engine,expire_on_commit=True)
