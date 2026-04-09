from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone
from sqlmodel import select
from jose import jwt,JWTError
import uuid
from sqlmodel import Session
from app.account.model import RefreshToken,User
secert_key="hello"
algo="HS256"
pwd = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

def hash_password(passw: str):
    return pwd.hash(passw)
def verfiy_password(plain_password,hash_password):
     return pwd.verify(plain_password,hash_password)
def create_acess_token(data:dict,expire_date:timedelta=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expire_date or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,secert_key,algorithm=algo)
def create_tokens(session:Session,user:User):
    access_token=create_acess_token(data={"sub":str(user.id)})
    refresh_token_str=str(uuid.uuid4())
    expire_at=datetime.now(timezone.utc)+timedelta(days=7)
    refresh_token=RefreshToken(user_id=user.id,
                               token=refresh_token_str,
                               expire_at=expire_at,

                               )
    session.add(refresh_token)
    session.commit()
    return {
        "access_token":access_token,
        "refresh_token":refresh_token_str,
        "expire_At":expire_at,
        "token_type":"bearer"
    }
def revised_token(session:Session,token:str):
    stmt=select(RefreshToken).where(RefreshToken.token==token)
    db_token=session.exec(stmt).first()
    if db_token and not db_token.revoked:
        expire_at=db_token.expire_at
        if expire_at.tzinfo is None:
            expire_at=expire_at.replace(tzinfo=timezone.utc)
        if expire_at>datetime.now(timezone.utc):
            stmt=select(User).where(User.id==db_token.user_id)
            return session.exec(stmt).first()
    return None
def decode_token(token:str):
    try:
       payload= jwt.decode(token,secert_key,algorithms=algo)
       return payload
    except JWTError:
        return None
def create_email_verification(user_id:int):
    expire=datetime.now(timezone.utc)+timedelta(hours=1)
    to_encode={"sub":str(user_id),"type":"verify","exp":expire}
    return jwt.encode(to_encode,secert_key,algorithm=algo)
def verify_token_and_get_user_id(token:str,token_type:str):
    try:
        payload=decode_token(token)
        if payload.get("type")!=token_type:
            return None
        return int(payload.get('sub'))
    except JWTError:
        return None
    
def get_user_email(session:Session,email:str):
    stmt=select(User).where(User.email==email)
    return session.exec(stmt).first()
def create_password_reset_token(user_id:int):
    expire=datetime.now(timezone.utc)+timedelta(hours=1)
    to_encode={"sub":str(user_id),"type":"reset","exp":expire}
    return jwt.encode(to_encode,secert_key,algorithm=algo)