from fastapi import FastAPI,BackgroundTasks,File,UploadFile
import os
import time
app=FastAPI()
#background task to save the file with simluated delay in devlompent phase .
def save_file(file_name:str,file_content:bytes):
    print(f"Strating  background task: Saving file {file_name}")
    time_now=time.time()
    time.sleep(5)
    with open (f"upload/{file_name}","wb") as f:
        f.write(file_content)
    end_time=time.time()
    print(f"Differnece b/w time_now and end_time :{time_now- end_time : .2f}second")
@app.post("/upload")
async def upload_file(file:UploadFile=File(...),back:BackgroundTasks=None):
    os.makedirs("upload",exist_ok=True)
    content= await file.read()
    back.add_task(save_file,file.filename,content)
    print(f"task is done  file name :{file.filename}")
    return {"msg":f"File '{file.filename}'  accepted for processing in the background"}
