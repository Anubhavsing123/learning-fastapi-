from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Pydantic Field

class Product(BaseModel):

    name: str = Field(
        title="Product Name",
        description="Describing about the product",
        max_length=100,
        min_length=3,
        pattern="^[A-Za-z0-9 ]+$"
    )

    price: float = Field(
        gt=0,
        title="Product Price",
        description="The price of the product in USD, must be greater than 0"
    )

    stock: int | None = Field(
        default=None,
        ge=0,
        title="No of product",
        description="The number of products available"
    )

@app.post("/product")
async def create_item(product: Product):
    return {"product": product}