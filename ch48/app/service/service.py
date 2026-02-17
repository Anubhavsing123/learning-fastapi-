from app.db.config import session
from app.user.model import User
from sqlalchemy import select,insert,delete
#create or insert user
def create_user(name:str,email:str,mobile:int):
    with session() as sess:
        user=User(name=name,email=email,phone=mobile)
        sess.add(user)
        sess.commit()
#read a user
def get_all():
    with session() as sess:
        user=select(User)
        res=sess.scalars(user)
        return res.all()
