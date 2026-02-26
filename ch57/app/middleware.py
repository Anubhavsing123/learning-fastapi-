from fastapi import Request
#first MIDDLEWARE

async def first_middleware(request:Request,call_next):
    if request.url.path.startswith("users"):
        print(" 1st Middleware : Before the request o the user")
        print (f" request method {request.method} and url {request.url}")
        response= await call_next(request)
        print(" 1st Middleware : Before the response of the user ")
        print(f" response status_code: {response.status_code}")
    
        return response
#second middleware
#middleware excute from buttom to top

async def second_middleware(request:Request,call_next):
    print(" 2nd Middleware : Before the request ")
    print (f" request method {request.method} and url {request.url}")
    response= await call_next(request)
    print(" 2nd Middleware : Before the response ")
    print(f" response status_code: {response.status_code}")
    return response