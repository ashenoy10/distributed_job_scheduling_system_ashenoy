import requests
import time
from celery import Celery
from .celery_worker import celery_app
import os

WORKER_ID = os.getenv("WORKER_ID", "worker_default")

# URL of the coordinator where worker registers its status
COORDINATOR_URL = "http://coordinator:8000/register-worker"

def register_worker():
    """Register the worker with the central coordinator."""
    payload = {"worker_id": WORKER_ID, "status": "available"}
    response = requests.post(COORDINATOR_URL, json=payload)
    if response.status_code == 200:
        print(f"Worker {WORKER_ID} registered successfully.")
    else:
        print(f"Failed to register worker {WORKER_ID}.")
        
def update_worker_status(status):
    """Update the status of the worker."""
    payload = {"worker_id": WORKER_ID, "status": status}
    response = requests.post(COORDINATOR_URL, json=payload)
    if response.status_code == 200:
        print(f"Worker {WORKER_ID} status updated to {status}.")
    else:
        print(f"Failed to update status for worker {WORKER_ID}.")

if __name__ == "__main__":
    # Register the worker at startup
    register_worker()
    
    # Start the Celery worker
    celery_app.worker_main(argv=[
        'worker', 
        '--loglevel=info'
    ])
