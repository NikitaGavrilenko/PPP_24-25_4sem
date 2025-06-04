from fastapi import WebSocket
from typing import Dict, Optional, Set
import json

class WebSocketManager:
    def __init__(self):
        # Храним соединения по схеме: user_id -> task_id -> WebSocket
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, user_id: str, task_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        self.active_connections[user_id][task_id] = websocket

    def disconnect(self, user_id: str, task_id: str):
        if user_id in self.active_connections and task_id in self.active_connections[user_id]:
            del self.active_connections[user_id][task_id]
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, user_id: str, task_id: str, message: dict):
        if user_id in self.active_connections and task_id in self.active_connections[user_id]:
            try:
                await self.active_connections[user_id][task_id].send_json(message)
            except Exception as e:
                print(f"Error sending message to {user_id}/{task_id}: {e}")
                self.disconnect(user_id, task_id)

ws_manager = WebSocketManager()