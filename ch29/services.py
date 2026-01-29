from db import engine
from table import user,post
from sqlalchemy import insert,select,update,delete
#insert or createuser
def create_user(name:str,email:str,phone:int):
    with engine.connect() as conn:
         # this context manger
        #(database connection and opeartion in the traction)
        stat=insert(user).values(name=name,email=email, phone=phone)
        conn.execute(stat)
        conn.commit()
def create_post(id:int,user:int,title:str,content:str):
    with engine.connect() as conn:
        sat=insert(post).values(id=id,user_id=user,title=title,content=content)
        conn.execute(sat)
        conn.commit()
#get user by id
def get_user_id(id:int):
    with engine.connect() as conn:
        stat=select(user).where(user.c.id==id)
        result=conn.execute(stat).first()
        return result
#get all the user
def get_user():
    with engine.connect() as conn:
        stat=select(user)
        result=conn.execute(stat).fetchall()
        return result
#get post by user_id
def get_post_id(id:int):
    with engine.connect() as conn:
        stat=select(user).where(post.c.user_id==id)
        result=conn.execute(stat).fetchall()
        return result
#updated user email
def updated_user_email(id:int,new_email:str):
    with engine.connect() as conn:
        stat=update(user).where(user.c.id==id).values(email=new_email)
        conn.execute(stat)
        conn.commit()
#delete the post
def delete_post(id:int):
    with engine.connect() as enn:
        stat=delete(post).where(post.c.id==id)
        enn.execute(stat)
        enn.commit()



