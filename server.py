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
    if "signature" in body:
        event = body.get("event")
        if event in ('livestart', 'liveend'):
            await manager.broadcast(json.dumps(body))
            print(
                f"live event: {body['event']} | Broadcaster: {body['broadcaster']['screen_id']}({body['broadcaster']['id']})"
            )
            print(
                f"signature is {'MATCH' if body['signature'] == webhook_signature else 'MISMATCH'} ({body['signature']})"
            )
            return {"message": "OK"}
        elif event in ('liveschedulecreate', 'livescheduleupdate', 'livescheduledelete'):
            print(
                f"live schedule event: {body['event']} | Broadcaster: {body['broadcaster']['screen_id']}({body['broadcaster']['id']})"
            )
            print(
                f"signature is {'MATCH' if body['signature'] == webhook_signature else 'MISMATCH'} ({body['signature']})"
            )
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