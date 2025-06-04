from fastapi import APIRouter
from pydantic import BaseModel
from app.services.tasks import start_encoding_task
from celery.result import AsyncResult

router = APIRouter(prefix="/api")

class EncodeRequest(BaseModel):
    data: str

@router.post("/encode")
async def start_encoding(request: EncodeRequest):
    user_id = "user123"
    task = start_encoding_task(user_id, request.data)
    return {
        "message": "Encoding started in background",
        "user_id": user_id,
        "task_id": task.id,
        "websocket_url": f"/ws/{user_id}/{task.id}"
    }


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)

    if not task.ready():
        return {
            "status": task.state,
            "progress": task.info.get('progress', 0) if task.info else 0
        }

    return {
        "status": task.state,
        "result": task.result
    }