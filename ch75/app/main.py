from fastapi import FastAPI,WebSocket,Query,Cookie,Depends,WebSocketException,status,WebSocketDisconnect
from typing import Annotated
from fastapi.responses import HTMLResponse
app=FastAPI()
html="""<!DOCTYPE html>
<html>
<body>
    <h1>WebSocket Chat</h1>
    
    <form action="" onsubmit="sendMessage(event)">
        <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
        <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
        <button type="button" onclick="connect(event)">Connect</button>
        <hr>
        <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
        <button type="submit">Send</button>
    </form>

    <ul id='messages'></ul>

    <script>
        var ws = null;

        function connect(event) {
            var itemId = document.getElementById("itemId");
            var token = document.getElementById("token");
            ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
            
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
        }

        function sendMessage(event) {
            var input = document.getElementById("messageText");
            ws.send(input.value);
            input.value = '';
            event.preventDefault();
        }
    </script>
</body>
</html>"""
@app.get("/")
async def get_root():
    return HTMLResponse(html)
# dependencies injection

async def cookie(
    sock: WebSocket, 
    sess: Annotated[str | None, Cookie()] = None, 
    token: Annotated[str | None, Query()] = None
):
    if sess is None and token is None:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION)
    return {"session": sess, "token": token}
@app.websocket("/items/{item_id}/ws") 
async def sock(websocket: WebSocket, item_id: str, ct: Annotated[dict, Depends(cookie)]):
    await websocket.accept()
    # ct is the dictionary returned from the 'cookie' dependency
    token_value = ct.get("token") or ct.get("session") 
    
    try:
        while True:
            data = await websocket.receive_text()
            # Combine the two required lines into one response, 
            # or send them sequentially if preferred.
            await websocket.send_text(f"Session cookie or query token value is: {token_value}")
            await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
    except WebSocketDisconnect:
        print("Connection closed")

