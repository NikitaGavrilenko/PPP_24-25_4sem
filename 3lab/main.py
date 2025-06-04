from fastapi import FastAPI, WebSocket
from app.api import endpoints
from app.api.websocket import websocket_endpoint

app = FastAPI()
app.include_router(endpoints.router)

@app.websocket("/ws/{user_id}/{task_id}")
async def websocket_handler(websocket: WebSocket, user_id: str, task_id: str):
    await websocket_endpoint(websocket, user_id, task_id)