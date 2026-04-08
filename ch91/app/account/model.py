from sqlmodel import SQLModel,Field,UniqueConstraint
from datetime import timezone,datetime
class UserBase(SQLModel):
    email:str
    username:str
    is_active:bool=True
    is_admin:bool=False
class Usercreate(UserBase):
    password:str
class UserOut(UserBase):
    id:int
class User(UserBase,table=True):
    __table_args__=(UniqueConstraint('email'),)
    id:int=Field(primary_key=True)
    hashed_password:str
    is_verified:bool=False
    create_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
class RefreshToken(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    user_id:int=Field(foreign_key='user.id')
    token:str
    expire_at:datetime
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    revoked:bool=False

