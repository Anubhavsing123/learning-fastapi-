from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
import uuid
from app.account.model import RefreshToken, User

secret_key = "hello"
algo = "HS256"

pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(passw: str):
    return pwd.hash(passw)

def verfiy_password(plain_password, hashed_password):
    return pwd.verify(plain_password, hashed_password)

def create_acess_token(data: dict, expire_date: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_date or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algo)

async def create_tokens(session: AsyncSession, user: User):
    access_token = create_acess_token(data={"sub": str(user.id)})
    refresh_token_str = str(uuid.uuid4())
    expire_at = datetime.now(timezone.utc) + timedelta(days=7)

    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expire_at=expire_at,
    )
    session.add(refresh_token)
    await session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "expire_At": expire_at,
        "token_type": "bearer"
    }

async def revised_token(session: AsyncSession, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    db_token = result.scalars().first()

    if db_token and not db_token.revoked:
        expire_at = db_token.expire_at
        if expire_at.tzinfo is None:
            expire_at = expire_at.replace(tzinfo=timezone.utc)
        if expire_at > datetime.now(timezone.utc):
            stmt = select(User).where(User.id == db_token.user_id)
            result = await session.execute(stmt)
            return result.scalars().first()
    return None

def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algo)
        return payload
    except JWTError:
        return None