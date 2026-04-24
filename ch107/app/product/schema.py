from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    title: str
    price: float
    stock: float


class ProductRead(ProductBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[float] = None