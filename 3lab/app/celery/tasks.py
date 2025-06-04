import time
import asyncio
from app.websocket.manager import ws_manager
from app.services.huffman import HuffmanCoder
import base64


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
        # Инициализация кодировщика
        huffman = HuffmanCoder()

        # Отправляем начальное уведомление
        asyncio.run(send_async_notification("STARTED"))

        # Шаг 1: Анализ данных (10%)
        frequency = huffman.build_frequency_dict(data)
        asyncio.run(send_async_notification("PROGRESS", progress=10))

        # Шаг 2: Построение дерева (30%)
        huffman.build_huffman_tree(frequency)
        asyncio.run(send_async_notification("PROGRESS", progress=30))

        # Шаг 3: Генерация кодов (50%)
        huffman.build_codes(huffman.build_huffman_tree(frequency))
        asyncio.run(send_async_notification("PROGRESS", progress=50))

        # Шаг 4: Кодирование данных (70%)
        encoded_bits, padding = huffman.encode_data(data)
        asyncio.run(send_async_notification("PROGRESS", progress=70))

        # Шаг 5: Преобразование в base64 (90%)
        # Конвертируем битовую строку в байты
        byte_array = bytearray()
        for i in range(0, len(encoded_bits), 8):
            byte = encoded_bits[i:i + 8]
            byte_array.append(int(byte, 2))

        encoded_base64 = base64.b64encode(byte_array).decode('utf-8')
        asyncio.run(send_async_notification("PROGRESS", progress=90))

        # Финальный результат
        final_result = {
            "encoded_data": encoded_base64,
            "huffman_codes": huffman.get_codes(),
            "padding": padding
        }
        asyncio.run(send_async_notification("COMPLETED", result=final_result))
        return final_result

    except Exception as e:
        asyncio.run(send_async_notification("FAILED", error=e))
        raise
