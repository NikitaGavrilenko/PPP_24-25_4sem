import time
import asyncio
from app.websocket.manager import ws_manager


def run_encoding_task(self, user_id: str, data: str):
    async def send_async_notification(status, progress=None, result=None):
        message = {
            "status": status,
            "task_id": self.request.id,
            "operation": "encode"
        }
        if progress is not None:
            message["progress"] = progress
        if result is not None:
            message["result"] = result

        await ws_manager.send_message(user_id, message)

    # Отправка уведомлений
    try:
        asyncio.run(send_async_notification("STARTED"))

        for progress in range(1, 101):
            time.sleep(0.1)
            asyncio.run(send_async_notification("PROGRESS", progress=progress))

        result = {"encoded_data": "base64_data"}
        asyncio.run(send_async_notification("COMPLETED", result=result))
        return result

    except Exception as e:
        print(f"Error in task: {e}")
        raise