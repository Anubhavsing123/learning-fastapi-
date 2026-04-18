from sqlalchemy.ext.asyncio import AsyncSession
from app.converter.model import *
from app.account.model import User
from app.converter.utilis import generate_api_key,convert_text
from sqlalchemy import select,delete
from fastapi import HTTPException
from app.converter.schema import *
async def generate_user_api_key(session:AsyncSession,user:User):
    await session.execute(delete(APIKey).where(APIKey.user_id==user.id))
    new_key=generate_api_key()
    key=APIKey(user_id=user.id,key=new_key)
    session.add(key)
    await session.commit()
    return new_key
async def get_user_api_key(session:AsyncSession,user:User):
    res= await session.scalars(select(APIKey).where(APIKey.user_id==user.id))
    key_obj=res.first()
    if not key_obj:
        raise HTTPException(status_code=404,detail="Not found api key")
    return key_obj.key

async def get_or_create_user_credits(session:AsyncSession,user_id:int):
    credit_obj=await session.scalar(select(UserCredit).where(UserCredit.user_id==user_id))
    if not credit_obj:
        credit_obj=UserCredit(user_id=user_id,credits=10)
        session.add(credit_obj)
        await session.commit()
        await session.refresh(credit_obj)
    return credit_obj
async def get_credit_request_list(session:AsyncSession,user:User):
    res= await session.scalars(select(CreditRequest).order_by(CreditRequest.created_at.desc()))
    return res.all()
async def  submit_credit_request(session:AsyncSession,user:User,credit:int):
    req=CreditRequest(user_id=user.id,credit_request=credit,status="pending")
    session.add(req)
    await session.commit()
    await session.refresh(req)
    return req
async def approved_credit_request(session:AsyncSession,request_id:int):
    req= await session.get(CreditRequest,request_id)
    if not req:
        raise HTTPException(status_code=404,detail="Not found")
    if req.status!="pending":
        raise HTTPException(status_code=400,detail="Already processed")
    credit_obj= await get_or_create_user_credits(session,req.user_id)
    credit_obj.credits+=req.credit_request
    req.status="approved"
    await session.commit()
    await session.refresh(req)
    return req
async def handle_conversion(session:AsyncSession,data:ConvertRequest,user:User):
    credit_obj=await get_or_create_user_credits(session,user.id)
    if credit_obj.credits<=0:
        raise HTTPException(status_code=402,detail="Out of Credit")
    try:
        result=convert_text(data.text,data.operation)
    except  ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    credit_obj.credits-=1
    await session.commit()
    return result

