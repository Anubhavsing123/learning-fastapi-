from fastapi import FastAPI
from app.user.router import router as r1
from app.product.router import router as r2
app=FastAPI()
app.include_router(r1,tags=["user"],prefix="/user")
app.include_router(r2,tags=["product"],prefix="/product")


@app.get("/root")
async def get_root():
    print("the directory root")
