from fastapi import FastAPI,Request
from app.middleware import *

app=FastAPI()
#first MIDDLEWARE
app.middleware("http")(second_middleware)
app.middleware("http")(first_middleware)



@app.get("/users")
async def get_user():
    print("the endpoints are")
    return {"data":"all ok data"}
@app.get("/product")
async def get_user_product():
    print("the endpoints are products")
    return {"data":"all ok data of the products"}