from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.manager import ws_manager

async def websocket_endpoint(websocket: WebSocket, user_id: str, task_id: str):
    await ws_manager.connect(user_id, task_id, websocket)
    try:
        while True:
            # Клиент может отправлять сообщения для управления задачей
            data = await websocket.receive_text()
            print(f"Message from {user_id}/{task_id}: {data}")
    except WebSocketDisconnect:
        print(f"Disconnected {user_id}/{task_id}")
        ws_manager.disconnect(user_id, task_id)