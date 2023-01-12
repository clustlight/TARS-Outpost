import os
from typing import List

import dotenv
from fastapi import WebSocket

dotenv.load_dotenv()
access_token = os.environ.get("TOKEN")

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        token = websocket.headers.get("notification-server-access-token")
        if token == access_token:
            self.connections.append(websocket)
        else:
            await websocket.close(1008, "Auth failed")

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)