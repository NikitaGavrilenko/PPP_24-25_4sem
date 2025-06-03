from app.websocket.manager import ws_manager
import time
from celery import current_task


def run_encoding_task(user_id: str, data: str):
    task_id = current_task.request.id

    # Синхронная обертка для асинхронного вызова
    def sync_notify(status, progress=None, result=None):
        import asyncio
        message = {
            "status": status,
            "task_id": task_id,
            "operation": "encode"
        }
        if progress is not None:
            message["progress"] = progress
        if result is not None:
            message["result"] = result
        asyncio.run(ws_manager.send_message(user_id, message))

    sync_notify("STARTED")

    for progress in range(1, 101):
        time.sleep(0.1)
        sync_notify("PROGRESS", progress=progress)

    result = {
        "encoded_data": "base64_data",
        "huffman_codes": {"test": "01"},
        "padding": 4
    }
    sync_notify("COMPLETED", result=result)
    return result