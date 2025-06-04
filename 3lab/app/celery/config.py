from app.celery import app
from celery import current_task

@app.task(name='app.celery.tasks.run_encoding_task_celery', bind=True)
def run_encoding_task_celery(self, user_id: str, data: str):
    from app.celery.tasks import run_encoding_task
    return run_encoding_task(self, user_id, data)