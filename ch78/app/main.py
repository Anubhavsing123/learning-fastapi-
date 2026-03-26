from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_table,SessionDep
from app.product.model import ProductCreate,ProductOut
from app.product.service import *
@asynccontextmanager
async def  lifespan(app:FastAPI):
    create_table()
    yield
app=FastAPI(lifespan=lifespan)
@app.post("/create_product",response_model=ProductOut)
async def post_product(sess:SessionDep,new_product:ProductCreate):
    prod= await create_product(sess,new_product)
    return prod
@app.get("/get_product",response_model=list[ProductOut])
async def get_product(sess:SessionDep):
    prod= await get_all_product(sess)
    return prod
@app.get("/get_id_product",response_model=ProductOut)
async def get_product_by_id(sess:SessionDep,new_id:int):
    pro= await get_product_id(sess,new_id)
    return pro
@app.delete("/delete_product")
async def delete(sess:SessionDep,new_id:int):
    prod= await delete_product(sess,new_id)
    return {}
