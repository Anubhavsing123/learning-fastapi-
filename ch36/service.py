from model import User,Post
from db import engine,session
from sqlalchemy import select,asc
#service.py for crud and business logic in sqlalchemyorm


#create te user
def create_user(name:str,email:str):
    with session() as sess:
      user=User(name=name,email=email)
      sess.add(user)
      sess.commit()
      sess.refresh(user)
      return user
#create post
def create_post(id:int,name:str,email:str):
    with session() as sess:
      post=Post(user_id=id,title=name,content=email)
      sess.add(post)
      sess.commit()
#read userid
def get_user_id(id:int):
   with session() as sess:
      user=sess.get_one(User,id)
      return user
#read post by user_id
def get_post_id(id:int):
   with session() as sess:
      stmt=select(Post).where(Post.id==id)
      post=sess.scalars(stmt).one()
      return post
#read all the user
def read_user():
   with session() as sess:
      stmt=select(User)
      user=sess.scalars(stmt).all()
      return user
#read all the post
def read_post(id:int):
   with session() as sess:
      user=sess.get(User,id)
      post=user.posts if user else []
      return post
#update email of user
def updated_email(id:int,new_email:str):
   with session() as sess:
      user=sess.get(User,id)
      if user:
         user.email=new_email
         sess.commit()
      return user
#delete the post
def delete_post(id:int):
   with session() as sess:
      post=sess.get(Post,id)
      if post:
         sess.delete(post)
         sess.commit()
#orde_by
def order_by():
   with session() as sess:
      stmt=select(User).order_by(asc(User.name))
      user=sess.scalars(stmt).all()
      return user

      
   
   
   
      

