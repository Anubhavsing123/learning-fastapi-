from fastapi import FastAPI
from app.middleware import Custom
app=FastAPI()
app.add_middleware(Custom,prefix="Custom")
@app.get("/user")
async def get_users():
    print("the endpoints are")
    return {"data":"all ok data"}
@app.get("/product")
async def get_user_product():
    print("the endpoints are products")
    return {"data":"all ok data of the products"}
