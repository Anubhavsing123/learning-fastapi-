from fastapi import FastAPI,File,UploadFile
from fastapi.responses  import HTMLResponse
from typing import Annotated
import os
import shutil
app=FastAPI()
#Html form testing
@app.get("/",response_class=HTMLResponse)
async def main():
    return """<html>
    <body>
    <h2>Multiple file upload(bytes)</h2>
    <form action="/file/" enctype="multipart/form-data" method="post" >
    <input name="file" type="file" multiple># name sholud match with the python side in loops

    <input value="upload" type="submit">
    </form>
    
    </body>
    </html>"""
@app.post("/file/")
async def creaed_upload_File(file:Annotated[list[UploadFile],File()]):
    save_file=[]
    os.makedirs("uploads",exist_ok=True)
    for  f in file:
        save_path=f"uploads/{f.filename}"
        with open (save_path,"wb") as buffer:
            shutil.copyfileobj(f.file,buffer)
            save_file.append({"filename":f.filename})
    return save_file


