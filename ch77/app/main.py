from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app=FastAPI()
app.mount("/css",StaticFiles(directory="app/static"),name="static")

#app.mount("/img",StaticFiles(directory="app/static"),name="images")

@app.get("/items")
async def home():
    return "Home"