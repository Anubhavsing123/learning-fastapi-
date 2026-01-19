from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from typing import Annotated
app=FastAPI()
#simple HTMl for test
@app.get ("/form",response_class=HTMLResponse)
async def form():
    # this form data is field not json
    return """
    <html>
    <body>
    <h2> login Form</h2>
    <form action="/login/" method=post>
    <label for ="username">UserName:</label>
    <br>
    <input type="text" id="username" name="username"><br>
    
    <label for ="password">password:</label><br>
    <input type="password" name="password" id="password"><br><br>
    <input type="submit" vaule="submit">
    
    </from>
    </body>
    </html>
  """
#without validation
# @app.post("/login/")
# async def login (username:Annotated[str,Form()],password:Annotated[str,Form()]):
#     return {"username":username,"password":len(password)}
#  with validation
@app.post("/login/")
async def login (username:Annotated[str,Form(min_length=3)],
                 password:Annotated[str,Form(min_length=3,max_length=12)]):
    return {"username":username,"password":len(password)}