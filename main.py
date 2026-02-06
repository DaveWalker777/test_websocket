from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>WebSocket Chat</title>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <form id="form">
        <input type="text" id="message" autocomplete="off" placeholder="Введите сообщение" />
        <button type="submit">Отправить</button>
    </form>
    <ol id="messages"></ol>
    <script>
        const ws = new WebSocket(`ws://${location.host}/ws`);
        const form = document.getElementById("form");
        const input = document.getElementById("message");
        const messages = document.getElementById("messages");

        form.addEventListener("submit", function(event) {
            event.preventDefault();
            const text = input.value.trim();
            if (!text) return;
            ws.send(JSON.stringify({message: text}));
            input.value = "";
        });

        ws.addEventListener("message", function(event) {
            const data = JSON.parse(event.data);
            const li = document.createElement("li");
            li.textContent = data.message;
            li.setAttribute("value", data.number);
            messages.appendChild(li);
        });
    </script>
</body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counter = 0
    try:
        while True:
            data = await websocket.receive_json()
            counter += 1
            await websocket.send_json({"number": counter, "message": data["message"]})
    except WebSocketDisconnect:
        pass
