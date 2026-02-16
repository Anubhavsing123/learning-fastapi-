from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
from app.user.model import User
from app.product.model import Product