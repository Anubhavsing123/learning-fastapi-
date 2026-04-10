from app.account.model import User,Usercreate
from app.account.utils import hash_password,verfiy_password
from fastapi import HTTPException
from sqlmodel import Session,select
from app.account.utils import create_email_verification,verify_token_and_get_user_id,get_user_email,create_password_reset_token

def create_user(session:Session,user:Usercreate):
    stmt=select(User).where(User.email==user.email)
    if session.exec(stmt ).first():
        raise HTTPException(status_code=400,detail="Alerady present")
    new_user=User(
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
        hashed_password=hash_password(user.password),
        is_verified=False
        
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
def auth_user(session:Session,email:str,password:str):
    stmt=select(User).where(User.email==email)

    print("Input:", email)
    print("User:", User)

    user=session.exec(stmt).first()
    if not user or not verfiy_password(password,user.hashed_password):
        return None
    return user
def email_verify(user:User):
    token=create_email_verification(user.id)
    link=f"http://127.0.0.1:8000/acc/verfiy/?token={token}"
    print(f"the verify link :{link}")
    return {"msg":"Verfication of email is completed"}
def verify_email_token(session:Session,token:str):
    user_id=verify_token_and_get_user_id(token,"verify")
    if not user_id:
        raise HTTPException(status_code=404,detail="Not Found")
    stmt=select(User).where(User.id==user_id)
    user=session.exec(stmt).first()
    user.is_verified=True
    session.add(user)
    session.commit()
    return {"msg":"Email is verified succefully !"}

def change_password(session:Session,user:User,new_password:str):
    user.hashed_password=hash_password(new_password)
    session.add(user)
    session.commit()
def password_reset(session:Session,email:str):
    user=get_user_email(session,email)
    if not user:
        raise HTTPException(status_code=404,detail="Not found")
    token=create_password_reset_token(user.id)
    link=f"http://127.0.0.1:8000/acc/reset/?token={token}"
    print(f"Reset Password:{link}")
    return {"msg":"Ok!"}
def reset_password_with_token(session:Session,token:str,new_pass:str):
    user_id=verify_token_and_get_user_id(token,"reset")
    if not user_id:
        raise HTTPException(status_code=404,detail="User_id not found")
    stmt=select(User).where(User.id==user_id)
    user=session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    change_password(session,user,new_pass)
    return {"msg":"password reset coplete"}



    