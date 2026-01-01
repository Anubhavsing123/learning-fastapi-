# how to make endpoints
from fastapi import FastAPI
app=FastAPI()
# @app.get("/")
# def main():
#     return {"Message":"hello world"}
# @app.get('/{id}')
# def main(id:int):
#     return {"kfmem":"mmeom"}
# @app.post('/post')
# async def main():
#     return {}
    
# @app.get("/path/{id:path}")
# async def main1(id:str):
#     return {"msg":id}
# @app.get('/path/{id}')
# async def main2(id:int):
#     return {"msg":"second"}
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file": file_path}