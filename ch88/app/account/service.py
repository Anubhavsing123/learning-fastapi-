from app.account.model import User,Usercreate
from app.account.utils import hash_password,verfiy_password
from fastapi import HTTPException
from sqlmodel import Session,select

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
