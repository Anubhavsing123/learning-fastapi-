from fastapi import FastAPI,Form,File,UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated
app=FastAPI()
import os
import uuid
import shutil
@app.get("/",response_class=HTMLResponse)
async def main():
    return """
    <html>
    <body>
    <h2>Single file upload(bytes)</h2>
    <form action="/file/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">

    <input value="upload" type="submit">
    </form>
    <h2>Single file upload(uploadfiles)</h2>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">

    <input value="upload" type="submit">
    </form>
    </body>
    </html>
"""
# @app.post("/file/")
# async def upload_file(file:Annotated[ bytes| None,File()]=None):
#     if not file:
#         return {"msg":"no file"}
#     return {"file_size":len(file)}
# with saving the file
@app.post("/file/")
async def upload_file(file:Annotated[ bytes| None,File()]=None):
    if not file:
        return {"msg":"no file"}
    filename=f'{uuid.uuid4()}.bin'#.bin extentions
    save_path=f'upload/{filename}'
    os.makedirs("upload",exist_ok=True)
    with open(save_path,'wb') as buffer:
        buffer.write(file)
    return {"file_size":len(file)}
#files without bytes
@app.post("/files")
async def upload_file(file:Annotated[UploadFile,File()]=None):
    if not file:
        return {"msg":"no file"}
    save_path=f"upload/{file.filename}"
    os.makedirs("upload",exist_ok=True)
    with open(save_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return {"filename":file.filename, "content-type":file.content_type}
        
