from app.account.model import User
from app.account.schema import UserCreate
from sqlalchemy import select
from  sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.account.utilis import (
    hash_password,
    verify_password,
   
    create_email_verification,
    verify_token_and_get_user_id,
    get_user_by_email,
    create_password_reset_token,
   
)
async def create_user(session:AsyncSession,user:UserCreate):
    stmt=select(User).where(User.email==user.email)
    res= await session.scalars(stmt)
    users=res.all()
    if users:
        raise HTTPException(status_code=400,detail="Alerady present")
    new_user=User(
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
        hash_password=hash_password(user.password),
        is_verified=False
        
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
async def auth_user(session:AsyncSession,email:str,password:str):
    stmt=select(User).where(User.email==email)

    print("Input:", email)
    print("User:", User)

    res= await session.scalars(stmt)
    user=res.first()
    if not user or not  verify_password(password,user.hash_password):
        return None
    return user
def email_verify(user:User):
    token=  create_email_verification(user.id)
    link=f"http://127.0.0.1:8000/acc/verify/?token={token}"
    print(f"the verify link :{link}")
    return {"msg":"Verfication of email is completed"}
async def verify_email_token(session:AsyncSession,token:str):
    user_id=verify_token_and_get_user_id(token,"verify")
    if not user_id:
        raise HTTPException(status_code=404,detail="Not Found")
    stmt=select(User).where(User.id==user_id)
    res=await session.scalars(stmt)
    user=res.first()
    
    user.is_verified=True
    session.add(user)
    await session.commit()
    return {"msg":"Email is verified succefully !"}
async def change_password(session:AsyncSession,user:User,new_password:str):
    user.hash_password=  hash_password(new_password)
    session.add(user)
    await session.commit()
async def password_reset(session:AsyncSession,email:str):
    user=await  get_user_by_email(session,email)
    if not user:
        raise HTTPException(status_code=404,detail="Not found")
    token=create_password_reset_token(user.id)
    link=f"http://127.0.0.1:8000/acc/reset/?token={token}"
    print(f"Reset Password:{link}")
    return {"msg":"Ok!"}
async def reset_password_with_token(session:AsyncSession,token:str,new_pass:str):
    user_id=  verify_token_and_get_user_id(token,"reset")
    if not user_id:
        raise HTTPException(status_code=404,detail="User_id not found")
    stmt=select(User).where(User.id==user_id)
    res= await session.scalars(stmt)
    user=res.first()
    print(user)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    await change_password(session,user,new_pass)
    return {"msg":"password reset coplete"}



    
