from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.account.service import create_user, auth_user
from app.account.utils import create_tokens
from app.account.schema import Usercreate
from app.db.config import SessionDep

router = APIRouter(prefix="/acc", tags=["account"])

@router.post("/register")
async def register(session: SessionDep, user: Usercreate):
    return await create_user(session, user)

@router.post("/login")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = await create_tokens(session, user)
    return token