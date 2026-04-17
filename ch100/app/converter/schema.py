from pydantic import BaseModel,Field
from datetime import datetime
class ConvertRequest(BaseModel):
    text:str=Field(...)
    operation:str=Field(...,description="upper or lower")
class ConvertResponse(BaseModel):
    result:str
class APIKeyOut(BaseModel):
    key:str
class CreditRequest(BaseModel):
    credits_request:int
class CreditRequestOut(BaseModel):
    id:int
    user_id:int
    credits_requested:int
    status:str
    created_at:datetime
    model_config={
        "from_attributes":True
    }
class CreditBalance(BaseModel):
    credit:int
class UserProfile(BaseModel):
    id:int
    email:str
    is_active:bool
    is_admin:bool
    is_verified:bool
    model_config={
        "from_attributes":True
    }