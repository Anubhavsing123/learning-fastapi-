from fastapi import APIRouter, Header, HTTPException, Depends  # type: ignore[import]
from typing import Annotated 
#m-1
async def verify(token:Annotated[str,Header()]):
    if token!="my_sceret_token":
        raise HTTPException(status_code=404,detail="Not found")
router=APIRouter(dependencies=[Depends(verify)])
@router.get("/items")
async def read_item():
    return {"ok":"data is correct"}
