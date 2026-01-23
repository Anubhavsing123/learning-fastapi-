from fastapi import FastAPI, UploadFile, File,Form
from fastapi.responses import HTMLResponse
from typing import Annotated
import os
import shutil
app = FastAPI()

# here we cannot use pydantic because of file upload
@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
    <body>

    <h2>Login Form</h2>

    <form action="/login/" method="post" enctype="multipart/form-data">

        <label for="username">UserName:</label><br>
        <input type="text" id="username" name="username"><br><br>

        <label for="password">Password:</label><br>
        <input type="password" name="password" id="password"><br><br>

        <h3>Upload File</h3>

        <label for="file">UploadFile</label><br>
        <input type="file" name="file" multiple ><br>

        <input type="submit" value="submit">

    </form>

    </body>
    </html>
    """
#single file
# @app.post("/login/")
# async def create_user_file(username:Annotated[str,Form()],
#                            file:Annotated[UploadFile |None,File()]=None):
#     response={"username":username}
#     if file:
#         save_path=f"upload/{file.filename}"
#         os.makedirs("upload",exist_ok=True)
#         with open (save_path,"wb") as f:
#             shutil.copyfileobj(file.file,f)
#             response["filename"]=file.filename
#     return response
#multiple file
@app.post("/login/")
async def create_user_file(username:Annotated[str,Form()],
                           file:Annotated[list[UploadFile] |None,File()]=None):
    response={"username":username,"filename":[]}
    if  not file:
        return {"mgs":"not found"}
    for f in file:
        save_file=[]
        save_path=f"upload/{f.filename}"
        os.makedirs("upload",exist_ok=True)
        with open (save_path,"wb") as bf:
            shutil.copyfileobj(f.file,bf)
            save_file.append({"file":f.file})
            response["filename"].append(f.filename)

            
    return response

