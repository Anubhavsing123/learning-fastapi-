from fastapi import FastAPI,Request
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app=FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware,allowed_hosts=["localhost","127.0.0.1"])
@app.get("/users")
async def get_user():
    print("the endpoints are")
    return {"data":"all ok data"}
@app.get("/product")
async def get_user_product():
    print("the endpoints are products")
    return {"data":"all ok data of the products"}