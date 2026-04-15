from fastapi import APIRouter,HTTPException
from app.account.service import *
router=APIRouter(prefix="/account",tags=["account"])
@router.post("/reg")
async def reg(name:str,email:str):
    return await create_user(name,email)
@router.get("/")
async def get_all():
    return await get_user_all()
@router.get("user/{user_id}")
async def get_all_id(user_id:str):
    user= await get_user_by_id(user_id)
    if not user:
        raise HTTPException(stauts_code=404,detail="Not found")
    return user
@router.put("/updated_user/{user_id}")
async def update_user(user_id:str,name:str=None,email:str=None):
    user=await updated_user(user_id,name,email)
    if not user:
        raise HTTPException(stauts_code=404,detail="Not Found")
    return user
@router.delete("delete_user/{user_id}")
async def delete(user_id:str):
    user= await delete_user(user_id)
    if not user:
            raise HTTPException(stauts_code=404,detail="Not found")
    return {"ok":"Succefull"}