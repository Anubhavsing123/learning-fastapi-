from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.account.model import User
from app.account.schema import UserCreate,UserOut
from app.db.config import SessionDep
from app.account.utilis import create_token,verify_access_token, revroked_token
from app.account.dependecies import get_current_user,required_admin
from app.account.service import (
    create_user,
    auth_user,
    email_verify,
    verify_email_token,
    change_password,
    reset_password_with_token,
    password_reset

)
router=APIRouter(prefix="/acc",tags=["account"])
@router.post("/reg",response_model=UserOut)
async def regsiter(session:SessionDep,user:UserCreate):
    return  await create_user(session,user)
@router.post('/login')
async def login(session:SessionDep,form_data:OAuth2PasswordRequestForm=Depends()):
    user= await auth_user(session,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid")
    token= await create_token(session,user)
    res=JSONResponse(content={"access_token":token["access_token"]})
    res.set_cookie("refresh_token",token["refresh_token"],httponly=True,secure=True,
                   samesite="lax",max_age=60*60*24*7)
    return res
@router.post("/refresh")
async def refersh_token(session:SessionDep,request:Request):
    token=request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=404,detail="Missing token")
    user= await verify_access_token(session,token)
    if not user:
        raise HTTPException(status_code=401,detail="Invaild or missing")
    return  await create_token(session,user)
@router.get("/me",response_model=UserOut)
async def get_user(user=Depends(get_current_user)):
    return user
@router.post("/email")
async def send_email(user=Depends(get_current_user)):
    return email_verify(user)
@router.get("/verify/")
async def verfiy_email(session:SessionDep,token:str):
    return  await verify_email_token(session,token)
@router.post('/change_password')
async def change_passwords(session:SessionDep,new_password:str,user=Depends(get_current_user)):
    await change_password(session,user,new_password)
    return {"msg":"ok!"}
@router.post("/forget_password")
async def forget_pass(session:SessionDep,email:str):
    return await password_reset(session,email)
@router.post('/reset')
async def reset_pass(session:SessionDep,token:str,new_pass:str):
    return await reset_password_with_token(session,token,new_pass)
@router.get('/admin')
async def is_admin(user=Depends(required_admin)):
    return user
@router.post('/logout')
async def logout(session:SessionDep,request:Request):
    token=request.cookies.get("refresh_token")
    if token:
         await revroked_token(session,token)
        
         
    response=JSONResponse(content={"detail":"logout"},status_code=200,)
    response.delete_cookie("refresh_token")
    return response

