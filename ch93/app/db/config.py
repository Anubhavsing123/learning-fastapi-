from sqlmodel import create_engine,SQLModel,Session
import os
from fastapi import Depends
from typing import Annotated
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path=os.path.join(BASE_DIR,"sqlite.db")
DATABASE_URL=f"sqlite:///{db_path}"
engine=create_engine(DATABASE_URL,echo=True)
def create_table():
    print("create database...")
    SQLModel.metadata.create_all(engine)
def get_Session():
    with Session(engine) as session:
        yield session

SessionDep=Annotated[Session,Depends(get_Session)]