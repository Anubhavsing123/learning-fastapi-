from pydantic import BaseModel, EmailStr

class Usercreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_admin: bool = False

class UserProfile(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    is_verified: bool
    model_config = {"from_attributes": True}