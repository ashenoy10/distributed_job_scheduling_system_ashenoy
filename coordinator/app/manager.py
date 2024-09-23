from worker_nodes.app.celery_worker import celery_app
import uuid

# In-memory storage for tracking jobs and statuses
jobs_status = {}

def submit_job(data):
    job_id = str(uuid.uuid4())
    task = celery_app.send_task("app.tasks.execute_job", args=[job_id, data])
    jobs_status[job_id] = "pending"
    return job_id

def update_job_status(job_id, status):
    jobs_status[job_id] = status

def get_job_status(job_id):
    return jobs_status.get(job_id)
