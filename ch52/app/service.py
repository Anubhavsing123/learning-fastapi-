from sqlmodel import Session,select
from db.db import engine
from db.model import User
def create_user(name:str,email:str):
    with Session(engine) as sess:
        user=User(name=name,email=email)
        sess.add(user)
        sess.commit()
        sess.refresh(user)
        return user
def get_all_user():
    with Session(engine) as sess:
        stmt=select(User)
        user=sess.exec(stmt)
        return user.all()
    
def get_user_id(user_id:int):
    with Session(engine) as sess:
        stmt=select(User).where(User.id==user_id)
        user=sess.exec(stmt).first()
        return user
def get_user_get(user_id:int):
    with Session(engine) as sess:
        stmt=sess.get(User,user_id)
        return stmt