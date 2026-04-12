from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone
from jose import jwt,JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import uuid
from app.account.model import RefreshToken,User
secert_key="hello"
algorithm="HS256"
pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
def create_acess_token(data:dict,expire_date:timedelta=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expire_date or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,secert_key,algorithm=algorithm)
async def create_token(session:AsyncSession,user:User):
   
    access_token=create_acess_token(data={"sub":str(user.id)})
    refresh_token_str=str(uuid.uuid4())
    expire_at=datetime.now(timezone.utc)+timedelta(days=7)
    refresh_token=RefreshToken(user_id=user.id,
                               token=refresh_token_str,
                               expire_at=expire_at,

                               )
    session.add(refresh_token)
    await session.commit()
    return {
        "access_token":access_token,
        "refresh_token":refresh_token_str,
        "expire_At":expire_at,
        "token_type":"bearer"
    }
async def verify_access_token(session:AsyncSession,token:str):
    stmt=select(RefreshToken).where(RefreshToken.token==token)
    result= await session.scalars(stmt)
    db_token=result.first()
    if db_token and not db_token.revoked:
        expire_at=db_token.expire_at
        if expire_at.tzinfo is None:
            expire_at=expire_at.replace(tzinfo=timezone.utc)
        if expire_at>datetime.now(timezone.utc):
            stmt=select(User).where(User.id==db_token.user_id)
            user_token=await session.scalars(stmt)
            return user_token.first()
        return None
def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            secert_key,
            algorithms=[algorithm]
        )
        print("Payload:", payload)
        return payload

    except JWTError as e:
        print("JWT ERROR:", e)
        return None
def create_email_verification(user_id:int):
    expire=datetime.now(timezone.utc)+timedelta(hours=1)
    to_encode={"sub":str(user_id),"type":"verify","exp":expire}
    return jwt.encode(to_encode,secert_key,algorithm=algorithm)
def verify_token_and_get_user_id(token: str, token_type: str):
    payload = decode_token(token)
    print(payload)

    if payload is None:
        return None

    if payload.get("type") != token_type:
        return None

    return int(payload["sub"])
async def get_user_by_email(session:AsyncSession,email:str):
    stmt=select(User).where(User.email==email)
    res= await session.scalars(stmt)
    return res.first()
def create_password_reset_token(user_id:int):
    expire=datetime.now(timezone.utc)+timedelta(hours=1)
    to_encode={"sub":str(user_id),"type":"reset","exp":expire}
    return jwt.encode(to_encode,secert_key,algorithm=algorithm)
async def  revroked_token(session:AsyncSession,token:str):
    stmt=select(RefreshToken).where(RefreshToken.token==token)
    res= await session.scalars(stmt)
    db_user=res.first()
    if db_user:
        db_user.revoked=True
        await session.commit()
