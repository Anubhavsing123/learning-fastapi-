from fastapi import APIRouter,Depends
from app.converter.schema import APIKeyOut,CreditBalance,CreditRequestOut,CreditRequestCreate,ConvertResponse,ConvertRequest
from app.db.config import SessionDep
from app.account.model import User
from typing import List
from app.converter.service import generate_user_api_key,get_user_api_key,get_or_create_user_credits,get_credit_request_list,submit_credit_request,approved_credit_request,handle_conversion
from app.account.dependences import get_current_user,required_admin
from app.converter.dependences import get_user_from_api_key
router=APIRouter(prefix="/api/convert",tags=["Converter"])
@router.post("/generate_api_key",response_model=APIKeyOut)
async def veiw_key(session:SessionDep,user:User=Depends(get_current_user)):
    key=await generate_user_api_key(session,user)
    return {"key":key}
@router.get("/me/api/veiw",response_model=APIKeyOut)
async def get_veiw_key(session:SessionDep,user:User=Depends(get_current_user)):
    key=await get_user_api_key(session,user)
    return {"key":key}
@router.get("/me/credit",response_model=CreditBalance)
async def get_my_credit(
    session:SessionDep,
    user:User=Depends(get_current_user)
):
    credit_obj=await get_or_create_user_credits(session,user.id)
    return {"credit":credit_obj.credits}
@router.get("/credit_request",response_model=List[CreditRequestOut])
async def list_requests(
    session:SessionDep,
    user:User=Depends(required_admin)
):
    return await get_credit_request_list(session,user)
@router.post("/buy-credits",response_model=CreditRequestOut)
async def buy_credit(session:SessionDep,data:CreditRequestCreate,user:User=Depends(get_current_user)):
    req=await submit_credit_request(session,user,data.credits_request)
    return req
@router.post("/approved/{request_id}",response_model=CreditRequestOut)
async def approved_credit(request_id:int,session:SessionDep,user:User=Depends(required_admin)):
    req= await approved_credit_request(session,request_id)
    return req
@router.post("/convert_text",response_model=ConvertResponse)
async def convert(session:SessionDep,data:ConvertRequest,user:User=Depends(get_user_from_api_key)):
    res= await handle_conversion(session,data,user)
    return {"result":res}