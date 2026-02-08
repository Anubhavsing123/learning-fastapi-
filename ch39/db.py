from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DB_URL="sqlite:///sqlite.db"
engine=create_engine(DB_URL,echo=True)
session=sessionmaker(bind=engine,expire_on_commit=False)