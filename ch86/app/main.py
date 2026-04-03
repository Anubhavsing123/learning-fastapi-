from fastapi import FastAPI
from decouple import config

#load enviroment variable from.env file

app=FastAPI()
@app.get("/")
def env_key():
    return{
        "api_screte":config("API_SCERET_KEY"),

        "PassWord":config("PASSWORD")

    }
