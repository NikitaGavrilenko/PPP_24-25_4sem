import websockets
import asyncio
import json
import uuid


class WebSocketClient:
    def __init__(self, user_id):
        self.user_id = user_id
        self.connections = {}

    async def connect_to_task(self, task_id):
        uri = f"ws://localhost:8000/ws/{self.user_id}/{task_id}"
        websocket = await websockets.connect(uri)
        self.connections[task_id] = websocket
        asyncio.create_task(self.listen_task(task_id))

    async def listen_task(self, task_id):
        while True:
            try:
                message = await self.connections[task_id].recv()
                data = json.loads(message)
                print(f"Task {task_id} update: {data}")

                if data.get("status") == "COMPLETED":
                    await self.connections[task_id].close()
                    del self.connections[task_id]
                    break

            except websockets.exceptions.ConnectionClosed:
                print(f"Connection closed for task {task_id}")
                break


async def main():
    user_id = "user123"
    client = WebSocketClient(user_id)

    for i in range(3):
        task_id = str(uuid.uuid4())
        print(f"Starting task {task_id}")
        await client.connect_to_task(task_id)

    # Ждем завершения всех задач
    while client.connections:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())