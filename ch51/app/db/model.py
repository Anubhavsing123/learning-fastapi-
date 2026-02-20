from sqlmodel import Field,SQLModel
#table name User
class User(SQLModel,table=True):
    id:int=Field(primary_key=True)
    name:str
    email:str