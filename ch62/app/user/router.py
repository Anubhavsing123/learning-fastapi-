from fastapi import APIRouter
#m-2
#router=APIRouter()

#@router.get("/user",tags=["user"])
#async def get_user():
   # print("all the user")
#@router.get("/user/{id}",tags=["custom"])
#async def get_user_id(id :int):
   # print(f" User _id :{id}")
router=APIRouter(tags=["user"])

@router.get("")
async def get_user():
    print("all the user")
@router.get("/{id}")
async def get_user_id(id :int):
    print(f" User _id :{id}")