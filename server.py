from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect

from websocket import ConnectionManager

manager = ConnectionManager()
app = FastAPI()


@app.post("/")
async def webhook_endpoint(body=Body(...)):
    data = str(body, "UTF-8")
    await manager.broadcast(data)
    return {"message": "OK"}


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)