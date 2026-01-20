from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
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
    # <label for ="name">Name:</label>
    # <br>
    # <input type="text" id="name" name="name"><br>
    
    <input type="submit" vaule="submit">
    
    </from>
    </body>
    </html>
  """
#pydantic with Form Data
# class FormDa(BaseModel):
#     username:str
#     password:str
# @app.post("/login/")
# async def form(login:Annotated[FormDa,Form()]):
#     return login
# #pydantic with form and viadtions and exrta for forbid
class FormData(BaseModel):
    model_config={"extra":"forbid"}
    username:str=Field(min_length=3)
    password:str=Field(min_lenght=3,max_length=12)

@app.post("/login/")
async def form(login:Annotated[FormData,Form()]):
    return login
  
    