from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy import String,Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from db import engine
class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    phone: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<User (id={self.id}, name={self.name}, email={self.email}, phone={self.phone})>"
    
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
async def drop_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

