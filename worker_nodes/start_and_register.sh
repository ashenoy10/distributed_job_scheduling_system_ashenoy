#!/bin/bash
# Start the Celery worker
sleep 1
celery -A app.celery_worker worker
python -c "from app.worker_utils import register_worker; register_worker()"