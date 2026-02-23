from sqlmodel import Field,SQLModel
class Prodcut(SQLModel,table=True):
    id:int=Field(primary_key=True)
    name:str