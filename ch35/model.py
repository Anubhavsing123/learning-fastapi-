from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,Table,Integer,Column
from db import engine
class Base(DeclarativeBase):
    pass
#user model/table
class userTable(Base):
    __tablename__="user"
    #editor know id is int throught by Mapped but mapped_column for db
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50),nullable=True)
    email:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    phone:Mapped[int]=mapped_column(nullable=False,unique=True)
    #one-to-many:user to Post no column created in sql used for making backward relationship
    #back_populates bulit two way relationship

    posts:Mapped[list["Post"]]=relationship("Post",back_populates="user",cascade="all,delete")
    #one to one user to proifle
    profile:Mapped["Profile"]=relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all,delete"
    )
   #many to many: user to address
    address:Mapped[list["Address"]]=relationship("Address",back_populates="user")

    def __rep__(self)->str:
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
    user:Mapped["userTable"]=relationship("user",back_populates="post")
    def __rep__self(self):
        return f"<Post id={self.id} title={self.title}"
#profile(one to one)
class Profile(Base):
    __tablename__="profile"
    id:Mapped[int]=mapped_column(primary_key=True)
    #one to many relationship 
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),
                                      nullable=True,unique=True)
    bio:Mapped[str]=mapped_column(String,nullable=True)
    
    #two way realtionship 
    user:Mapped["userTable"]=relationship("user",back_populates="profile")
    def __rep__self(self):
        return f"<Profile id={self.id} bio={self.bio} user_id={self.user_id}"
#address (Many -Many)
class Address(Base):
    __tablename__="add"
    id:Mapped[int]=mapped_column(primary_key=True)
    street:Mapped[str]=mapped_column(String,nullable=False)
    country:Mapped[str]=mapped_column(String,nullable=False)
    user:Mapped[list["userTable"]]=relationship("user",back_populates="add")
    #for many-many accociation table is must
    user_acc=Table(
        "user_add_acc",
        Base.metadata,
        Column("user_id",Integer, ForeignKey("user.id", ondelete="CASCADE"), 
               primary_key=True),
        Column("address_id",Integer,ForeignKey("add.id",ondelete="CASCADE"),
               primary_key=True)
    )

    def __rep__(self):
        return f"<Address street={self.street} country={self.country} id={self.id}>"


#create table
def create_table():
  Base.metadata.create_all(engine)
#drop table
def drop_table():
    Base.metadata.drop_all(engine)