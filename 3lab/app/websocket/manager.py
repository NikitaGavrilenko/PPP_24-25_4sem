from fastapi import WebSocket
from typing import Dict
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def send_progress(self, user_id: str, progress: int):
        if conn := self.active_connections.get(user_id):
            await conn.send_json({
                'type': 'progress',
                'progress': progress
            })

ws_manager = WebSocketManager()