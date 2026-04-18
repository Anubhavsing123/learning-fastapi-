from app.account.model import User
from app.account.schema import Usercreate
from app.account.utils import hash_password, verfiy_password
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, user: Usercreate):
    stmt = select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Already present")

    new_user = User(
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
        hashed_password=hash_password(user.password),
        is_verified=False
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def auth_user(session: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or not verfiy_password(password, user.hashed_password):
        return None
    return user