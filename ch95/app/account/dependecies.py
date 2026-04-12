from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy import select
from app.db.config import SessionDep
from app.account.utilis import decode_token
from app.account.model import User
oauth=OAuth2PasswordBearer(tokenUrl='/acc/login')
async def get_current_user(session:SessionDep,token:str=Depends(oauth))->User:
    payload=decode_token(token)    
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentails") 
    stmt=select(User).where(User.id==int(payload.get('sub')))
    res= await session.scalars(stmt)
    user=res.first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    return user
async def required_admin(user:User=Depends(get_current_user))->User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not admin")
    return user
