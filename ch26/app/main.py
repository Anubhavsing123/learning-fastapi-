from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app=FastAPI()
name={
    "apple":"REd light color",
    "grapes":"green  in color"
}
# create Exceptions

@app.exception_handler(RequestValidationError)
async def main(request,exc:RequestValidationError):
    return PlainTextResponse(str(exc),status_code=404)
@app.get("/{id}")
async def main(id:int):
    return id
    


