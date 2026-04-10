from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlmodel import select
from app.account.model import User
from app.db.config import SessionDep
from app.account.utils import decode_token

oauth2=OAuth2PasswordBearer(tokenUrl="/acc/login")
async def get_current_user(session:SessionDep,token:str=Depends(oauth2)):
    payload=decode_token(token)    
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid credentails") 
    stmt=select(User).where(User.id==int(payload.get('sub')))
    user=session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    return user
def required_admin(user:User=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403,detail="Not admin")
    return user

