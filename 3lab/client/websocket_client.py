import websockets
import asyncio
import json


async def listen_notifications(user_id: str):
    uri = f"ws://localhost:8000/ws/{user_id}"

    async with websockets.connect(uri) as websocket:
        print(f"Connected as user {user_id}")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Notification: {data}")


if __name__ == "__main__":
    asyncio.run(listen_notifications("user123"))