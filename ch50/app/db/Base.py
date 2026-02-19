from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
class Base(AsyncAttrs,DeclarativeBase):
    pass

from app.user import model
from app.product.model import Product