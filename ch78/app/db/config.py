from sqlmodel import SQLModel, create_engine, Session
import os
from fastapi import Depends
from typing import Annotated
Base_Dir=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path=os.path.join(Base_Dir,"sqlite.db")
DATABASE_URL=f"sqlite:///{db_path}"
engine=create_engine(DATABASE_URL,echo=True)
def create_table():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
SessionDep=Annotated[Session,Depends(get_session)]



