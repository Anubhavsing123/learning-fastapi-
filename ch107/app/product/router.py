from fastapi import APIRouter
from app.db.config import SessionDep
from app.product.schema import ProductBase, ProductUpdate, ProductRead
from app.product.service import (
    create_product,
    get_all_products,
    get_product,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/product", tags=["products"])


@router.post("/create_product", response_model=ProductRead,status_code=201)
async def create_products(session: SessionDep, product: ProductBase):
    return await create_product(session, product)


@router.get("/", response_model=list[ProductRead],status_code=200)
async def get_products(session: SessionDep):
    return await get_all_products(session)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(product_id: int, session: SessionDep):
    return await get_product(product_id, session)


@router.put("/{product_id}", response_model=ProductRead,status_code=201)
async def updated_product(
    product_id: int,
    data: ProductUpdate,
    session: SessionDep,
):
    return await update_product(product_id, data, session)


@router.delete("/delete/{product_id}")
async def delete_product_by_id(product_id: int, session: SessionDep):
    return await delete_product(product_id, session)