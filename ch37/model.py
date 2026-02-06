from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,Table,Integer,Column
from db import engine
#model/table file
class Base(DeclarativeBase):
    pass
#user model/table
class User(Base):
    __tablename__="user"
    #editor know id is int throught by Mapped but mapped_column for db
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50),nullable=True)
    email:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    
    #one-to-many:user to Post no column created in sql used for making backward relationship
    #back_populates bulit two way relationship

    posts:Mapped[list["Post"]]=relationship("Post",back_populates="user",
                                            cascade="all,delete")
  
    def __repr__(self)->str:
        return f"<user(id={self.id},name={self.name},email={self.email})>"
#post one- to-many

class Post(Base):
    __tablename__="post"
     #editor know id is int throught by Mapped but mapped_column for db
    id:Mapped[int]=mapped_column(primary_key=True)
    #one to many relationship
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE")
                                      ,nullable=True)
    title:Mapped[str]=mapped_column(String,nullable=True)
    content:Mapped[str]=mapped_column(String,nullable=True)
    #two way realtionship
    user:Mapped["User"]=relationship("User",back_populates="posts")
    def __repr__(self):
        return f"<Post id={self.id} title={self.title} content={self.content}>"
def create_table():
  Base.metadata.create_all(engine)
