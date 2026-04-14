from app.account.service import create_user
from fastapi import APIRouter
from app.db.config import SessionDep
router=APIRouter(prefix="/acc",tags=["acc"])
@router.post('/reg')
async def reg(session:SessionDep,name:str,email:str):
   return await create_user(session,name,email)    
