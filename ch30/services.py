from db import engine
from table import user,post
from sqlalchemy import insert,select,func
#insert or createuser
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
# get usr by odered name
# def get_user_orderd_name():
#     with engine.connect() as conn:
#         stmt=select(user).order_by(asc(user.c.name))
#         res=conn.execute(stmt).fetchall()
        # return res
#  #get  odered by post
# def get_user_orderd_name():
#     with engine.connect() as conn:
#         stmt=select(post).order_by(desc(post.c.id))
#         res=conn.execute(stmt).fetchall()
#         return res
# #get  odered by post
# def get_user_orderd_name():
#     with engine.connect() as conn:
#         stmt=select(post).order_by(asc(post.c.id))
#         res=conn.execute(stmt).fetchall()
        # return res
#get  group_by by post
def get_post_goup_by():
    with engine.connect() as conn:
        stmt=select(post.c.user_id,func.count(post.c.id).label("total post"))
        .group_by(post.c.user_id)
        res=conn.execute(stmt).fetchall()
        return res
    
