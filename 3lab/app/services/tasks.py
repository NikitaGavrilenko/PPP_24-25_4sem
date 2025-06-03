from app.celery import app as celery_app

def start_encoding_task(user_id: str, data: str):
    return celery_app.send_task(
        'app.celery.tasks.run_encoding_task',  # Должно совпадать с name в @app.task
        args=(user_id, data),
        kwargs={}
    )