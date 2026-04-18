from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy import select
from fastapi import HTTPException,status
from app.account.model import User
from app.db.config import SessionDep
from app.account.utils import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/acc/login")

async def get_current_user(session: SessionDep, token: str = Depends(oauth2)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stmt = select(User).where(User.id == int(payload.get("sub")))
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
async def required_admin(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
