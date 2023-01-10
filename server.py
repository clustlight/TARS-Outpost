import json
import os

import dotenv
from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect

from websocket import ConnectionManager

dotenv.load_dotenv()

manager = ConnectionManager()
app = FastAPI()

webhook_signature = os.environ.get("WEBHOOK_SIGNATURE")

@app.post("/")
async def webhook_endpoint(body=Body(...)):
    if "signature" in body and "event" in body and "movie" in body and "broadcaster" in body:
        if body["signature"] == webhook_signature:
            if body["event"] == "livestart" or body["event"] == "liveend":
                await manager.broadcast(json.dumps(body))
                return {"message": "OK"}


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)