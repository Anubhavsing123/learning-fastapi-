from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone
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
