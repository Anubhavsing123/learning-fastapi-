from fastapi import FastAPI,Cookie
from typing import Annotated
#cookie parameter
app=FastAPI()
@app.get("/product")
async def get_pro(session_id: Annotated[str|None,Cookie()]=None):
    if session_id:
        return {"message":f"Recomm. session {session_id}","session_id":session_id}
    return {"msg":"no seesion id "}
