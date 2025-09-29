# routers/websockets.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter(tags=["WebSockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        text = json.dumps(message)
        for conn in self.active_connections:
            await conn.send_text(text)

manager = ConnectionManager()

@router.websocket("/ws/bookings")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text() # echo or ping if desired
            await websocket.send_text(f"server received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)