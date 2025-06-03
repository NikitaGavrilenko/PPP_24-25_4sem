from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.manager import ws_manager

async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        ws_manager.disconnect(user_id)