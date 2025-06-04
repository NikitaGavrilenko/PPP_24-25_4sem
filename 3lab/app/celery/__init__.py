from celery import Celery

app = Celery(
    'tasks',
    broker='sqla+sqlite:///celery_broker.db',
    backend='db+sqlite:///celery_results.db',
    include=['app.celery.tasks', 'app.celery.config']  # Добавьте оба модуля!
)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_proc_alive_timeout=30,
    broker_connection_retry_on_startup=True
)