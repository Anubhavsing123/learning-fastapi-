from fastapi import APIRouter,Depends,HTTPException
from app.account.service import create_user,auth_user
from app.account.model import *
from app.db.config import SessionDep
from fastapi.responses import JSONResponse
from app.account.utils import create_tokens
from fastapi.security import OAuth2PasswordRequestForm
router=APIRouter(prefix="/acc",tags=["account"])
@router.post("/reg",response_model=UserOut)
async def regsiter(session:SessionDep,user:Usercreate):
    return create_user(session,user)
@router.post('/login')
async def login(session:SessionDep,form_data:OAuth2PasswordRequestForm=Depends()):
    user=auth_user(session,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid")
    token=create_tokens(session,user)
    res=JSONResponse(content={"access_token":token["access_token"]})
    res.set_cookie("refresh_token",token["refresh_token"],httponly=True,secure=True,
                   samesite="lax",max_age=60*60*24*7)
    return res