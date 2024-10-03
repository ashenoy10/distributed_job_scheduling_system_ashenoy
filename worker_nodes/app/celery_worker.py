from celery import Celery 

celery_app = Celery(
    'app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Import the tasks to ensure they are registered
from . import celery_tasks
