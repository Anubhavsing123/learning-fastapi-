from fastapi import Request
#first MIDDLEWARE

async def user_middleware(request: Request, call_next):

    if request.url.path.startswith("/users"):
        print("User Middleware : Before the request of the user")
        print(f"request method {request.method} and url {request.url}")
        response = await call_next(request)
        return response
    else :
        print(f" User Middleware Skipping middleware for {request.url.path}")
        response = await call_next(request)
        return response
async def product_middleware(request:Request,call_next):
    if request.url.path.startswith("/product"):
        print("product Middleware : Before the request of the product")
        print(f"request method {request.method} and url {request.url}")
        response = await call_next(request)
        return response
    else :
        print(f" Product Middleware Skipping middleware for {request.url.path}")
        response = await call_next(request)
        return response
async def my_middleware(request:Request,call_next):
    
        print("My Middleware : Before the request of the product")
        print(f"My method {request.method} and url {request.url}")
        response = await call_next(request)
        return response 