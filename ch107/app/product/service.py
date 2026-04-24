from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.model import Product
from app.product.schema import ProductBase, ProductUpdate


async def create_product(session: AsyncSession, product: ProductBase):
    new_product = Product(
        title=product.title,
        price=product.price,
        stock=product.stock,
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def get_all_products(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def get_product(product_id: int, session: AsyncSession):
    product = await session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: AsyncSession,
):
    product = await session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.title is not None:
        product.title = data.title

    if data.price is not None:
        product.price = data.price

    if data.stock is not None:
        product.stock = data.stock

    await session.commit()
    await session.refresh(product)

    return product


async def delete_product(product_id: int, session: AsyncSession):
    product = await session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    await session.commit()

    return {"detail": "Product deleted successfully"}