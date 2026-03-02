from fastapi import APIRouter
router=APIRouter()
@router.get("/product")
async def get_user():
    print("all the product")
@router.get("/product/{id}")
async def get_user_id(id :int):
    print(f" prodcut _id :{id}")