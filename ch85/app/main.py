from fastapi import FastAPI
from dotenv import load_dotenv
import os
#load enviroment variable from.env file
load_dotenv()
app=FastAPI()
@app.get("/")
def env_key():
    return{
        "api_screte":os.getenv("API_SCERET_KEY"),

        "PassWord":os.getenv("PASSWORD")

    }
