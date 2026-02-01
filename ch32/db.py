from sqlalchemy import create_engine
DB_URL="sqlite:///../sqlite.db"
engine=create_engine(DB_URL,echo=True)
