from app.account.model import User
from typing import List

from beanie.operators import In
async def create_user(name:str,email:str)->User:
    user=User(name=name,email=email)
    await user.insert()
    return user
async def get_user_by_id(user_id:str):
    return await User.get(user_id)
async def get_user_all()->List[User]:
    return await User.find_all().to_list()
async def updated_user(user_id:str,name:str=None,email:str=None)->User:
    user=await User.get(user_id)
    
    if user:
        if name:
            user.name=name
        if email:
            user.email=email
        await user.save()
    return user 
async def delete_user(user_id:str)-> bool:
    user=await User.get(user_id)
    if user:
        await user.delete()
        return True
    return False


