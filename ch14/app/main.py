from fastapi import FastAPI,Header
from typing import Annotated,List
app=FastAPI()
# Header Parameter
# @app.get("/product")
# async def main(user_agent:Annotated[str| None,Header()]=None):
#     return user_agent
#C:\>curl -H "user-agent: abc124" http://127.0.0.1:8000/product
# "abc124"

#handling duplicate header
@app.get("/product")
async def main(user_agent:Annotated[List[str]| None,Header()]=None):
    return {"user_agent":user_agent or []}
#C:\>curl -H "user-agent: abc124" -H "user-agent: abc12435" http://127.0.0.1:8000/product
# {"user_agent":["abc124","abc12435"]}
