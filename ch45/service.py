from model import User
from db import session_maker
from sqlalchemy import select
#insert or create_user
async def create_user(name:str,email:str,phone:int):
    async with session_maker() as sess:
        user=User(name=name,email=email,phone=phone)
        sess.add(user)
        await sess.commit()
#read user by id
async def get_user_by_id(user_id:int):
    async with session_maker() as sess:
        user= await sess.get_one(User,user_id)
        return user
#read user 
async def get_user_all():
    async with session_maker() as sess:
        user= select(User)
        res= await sess.scalars(user)
        return res.all()
async def update_user(user_id:int,new_email:str):
    async with session_maker() as sess:
        user= await sess.get(User,user_id)
        if user:
            user.email=new_email
            await sess.commit()
            return user
#delete
async def delete_user(user_id:int):
    async with session_maker() as sess:
        user= await sess.get_one(User,user_id)
        if user:
            await sess.delete(user)
            await sess.commit()



