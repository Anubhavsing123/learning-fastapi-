from fastapi import APIRouter
from app.account.service import create_user
from app.db.config import SessionDep
router=APIRouter(prefix="/user",tags=["account"])
@router.post("/register")
async def register(session:SessionDep,name:str,email:str):
    return await create_user(session,name,email)