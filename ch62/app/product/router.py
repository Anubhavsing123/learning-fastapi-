from fastapi import APIRouter
router=APIRouter()
@router.get("")
async def get_user():
    print("all the product")
@router.get("/{id}")
async def get_user_id(id :int):
    print(f" prodcut _id :{id}")