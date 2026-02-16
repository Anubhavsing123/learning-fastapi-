from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path=os.path.join(BASE_DIR,"sqlite.db")
DATABASE_URL=f"sqlite:///{db_path}"
engine=create_engine(DATABASE_URL)
