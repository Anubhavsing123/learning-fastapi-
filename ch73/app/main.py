from fastapi import FastAPI,WebSocket
from fastapi.responses import HTMLResponse
app=FastAPI()
html="""
<!DOCTYPE html>
<html> 
<head>
<title> chat</title>
</head>
<body>
<h1>webscoket chat</h1>
<form action="" onsubmit="sendMessage(event)">
<input type="text" id="messageText" autocomplete="off"/>
<button> Send</button>
</form>
<ul id="msgs">
</ul>
<script>
var ws=new WebSocket("ws://localhost:8000/ws")
ws.onmessage=function(event){
 var msgs=document.getElementById("msgs")
 var msg=document.createElement("li")
 var content=document.createTextNode(event.data)
 msg.appendChild(content)
 msgs.appendChild(msg)

 };
 function sendMessage(event){
 var input=document.getElementById("messageText")
 ws.send(input.value)
 input.value=""
 event.preventDefault()
 }
 </script>
 </body>
 </html>

 """
@app.get("/")
async def home():
    return HTMLResponse(html)
@app.websocket("/ws")
async def socket_point(websock:WebSocket):
    await websock.accept()
    while True:
        data= await  websock.receive_text()
        await websock.send_text(f'Message to display :{data}')
