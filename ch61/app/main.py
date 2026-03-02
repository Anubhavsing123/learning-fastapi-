from fastapi import FastAPI
from app.user.router import router as r1
from app.product.router import router as r2
app=FastAPI()
#M-1
#app.include_router(r1,tags=["user"])
#app.include_router(r2,tags=["product"])
#M-2
app.include_router(r1)
app.include_router(r2)
@app.get("/root")
async def get_root():
    print("the directory root")
