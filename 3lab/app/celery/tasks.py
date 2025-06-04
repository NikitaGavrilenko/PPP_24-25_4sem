import time
import asyncio
from app.websocket.manager import ws_manager


def run_encoding_task(self, user_id: str, data: str):
    async def send_async_notification(status, progress=None, result=None, error=None):
        message = {
            "status": status,
            "task_id": self.request.id,
            "operation": "encode"
        }

        if progress is not None:
            message["progress"] = progress

        if result is not None:
            message["result"] = {
                "encoded_data": result["encoded_data"],
                "huffman_codes": result.get("huffman_codes", {}),
                "padding": result.get("padding", 0)
            }

        if error is not None:
            message["error"] = str(error)

        await ws_manager.send_message(user_id, self.request.id, message)

    try:
        # Отправляем начальное уведомление
        asyncio.run(send_async_notification("STARTED"))

        # Имитация процесса кодирования
        result_data = {"encoded_data": "", "huffman_codes": {}, "padding": 0}

        for progress in range(1, 101):
            time.sleep(0.1)
            # Обновляем результат на каждом шаге
            result_data["encoded_data"] = f"partial_{progress}"
            result_data["huffman_codes"] = {str(i): bin(i)[2:] for i in range(progress)}
            result_data["padding"] = progress % 8

            asyncio.run(send_async_notification("PROGRESS", progress=progress))

        # Финальный результат
        final_result = {
            "encoded_data": "base64_encoded_final",
            "huffman_codes": {"A": "101", "B": "110", "C": "1110"},
            "padding": 4
        }
        asyncio.run(send_async_notification("COMPLETED", result=final_result))
        return final_result

    except Exception as e:
        asyncio.run(send_async_notification("FAILED", error=e))
        raise