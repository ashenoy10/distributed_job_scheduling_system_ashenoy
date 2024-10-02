import requests
import os

WORKER_ID = os.getenv("WORKER_ID")

# URL of the coordinator where worker registers its status
COORDINATOR_URL = "http://coordinator:8000/register-worker"

def register_worker():
    """Register the worker with the central coordinator."""
    payload = {"worker_id": WORKER_ID, "status": "available", "job_id": ""}
    response = requests.post(COORDINATOR_URL, json=payload)
    if response.status_code == 200:
        print(f"Worker {WORKER_ID} registered successfully.")
    else:
        print(f"Failed to register worker {WORKER_ID}.")
        
def update_worker_status(status, job_id=""):
    """Update the status of the worker."""
    payload = {"worker_id": WORKER_ID, "status": status, "job_id": job_id}
    response = requests.post(COORDINATOR_URL, json=payload)
    if response.status_code == 200:
        print(f"Worker {WORKER_ID} status updated to {status}.")
    else:
        print(f"Failed to update status for worker {WORKER_ID}.")
    

def request_worker_status(WORKER_ID):
    """Update the status of the worker."""