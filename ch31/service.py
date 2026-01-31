from table import post,user
from db import engine
from sqlalchemy import insert,select
def create_user(name:str,email:str,phone:int):
    with engine.connect() as conn:
         # this context manger
        #(database connection and opeartion in the traction)
        stat=insert(user).values(name=name,email=email, phone=phone)
        conn.execute(stat)
        conn.commit()
def create_post(user:int,title:str,content:str):
    with engine.connect() as conn:
        sat=insert(post).values(user_id=user,title=title,content=content)
        conn.execute(sat)
        conn.commit()
#join the post and user
def join_user_post():
    with engine.connect() as conn:
        sat=select(post.c.id,post.c.title,user.c.name.label("authour_name")).join(
            user,post.c.user_id==user.c.id
        )
        res=  conn.execute(sat).fetchall()
        return res
