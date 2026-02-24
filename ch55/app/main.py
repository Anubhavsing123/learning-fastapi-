from fastapi import FastAPI,Request
app=FastAPI()
#CREATE MIDDLEWARE
@app.middleware("http")
async def my_midd(request:Request,call_next):
    print("Middleware : Before the request ")
    print (f" request method {request.method} and url {request.url}")
    response= await call_next(request)
    print("Middleware : Before the response ")
    print(f" response status_code: {response.status_code}")
    return response
@app.get("/users")
async def get_user():
    print("the endpoints are")
    return {"data":"all ok data"}
@app.get("/product")
async def get_user_product():
    print("the endpoints are products")
    return {"data":"all ok data of the products"}