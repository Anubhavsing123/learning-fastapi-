from sqlmodel import Session,select
from app.db.config import engine
from app.user.model import User
def create_user(name:str,email:str):
    user=User(name=name,email=email)
    with Session(engine) as sess:
        sess.add(user)
        sess.commit()
        sess.refresh(user)
        return user
def get_all_user():
    with Session(engine) as sess:
        user=select(User)
        stmt=sess.exec(user)
        return stmt.all()