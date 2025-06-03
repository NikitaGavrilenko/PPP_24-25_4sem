from celery import Celery
from app.celery import app

@app.task(bind=True)
def run_encoding_task_celery(self, user_id: str, data: str):
    from app.celery.tasks import run_encoding_task
    return run_encoding_task(user_id, data)