from fastapi import APIRouter,Depends
from app.converter.schema import APIKeyOut
from app.db.config import SessionDep
from app.account.model import User
from app.converter.service import generate_user_api_key
from app.account.dependences import get_current_user
router=APIRouter(prefix="/api/convert",tags=["Converter"])
@router.post("/generate_api_key",response_model=APIKeyOut)
async def veiw_key(session:SessionDep,user:User=Depends(get_current_user)):
    key=await generate_user_api_key(session,user)
    return {"key":key}
