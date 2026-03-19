from fastapi import FastAPI,BackgroundTasks
app=FastAPI()
def write_email (email:str,message:str=""):
    with open("login.txt",mode="w") as f:
        content=f"notification  for {email}:{message}"
        f.write(content)
@app.post("/notfy/{email}")
async def background(email:str,back:BackgroundTasks):
    back.add_task(write_email,email,message="tsk is done ")
    return {"msg":"ok done"}