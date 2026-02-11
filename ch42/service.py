from db import engine
from table import user
from sqlalchemy import select,insert,update,delete
#create a user or insert
async def create_user(name:str,email:str,mobile:str):
    async with engine.connect() as conn:
        stmt=insert(user).values(name=name,email=email,phone=mobile)
        await conn.execute(stmt)
        await conn.commit()
# select the user by id
async def get_user_id(id:int):
    async with engine.connect() as conn:
        stmt=select(user).where(user.c.id==id)
        result =await conn.execute(stmt)
        return result.first()
#select all the user
async def get_all_user():
    async with engine.connect()  as conn:
        stmt=select(user)
        result= await conn.execute(stmt)
        return result.fetchall()
#updated the email
async def updated_email(id:int,new_email:str):
    async with engine.connect() as conn:
        stmt=update(user).where(user.c.id==id).values(email=new_email)
        await conn.execute(stmt)
        await conn.commit()
#delete the user
async def delete_user(id:int):
    async with engine.connect()as conn:
        stmt=delete(user).where(user.c.id==id)
        await conn.execute(stmt)
        await conn.commit()

           
        
        


