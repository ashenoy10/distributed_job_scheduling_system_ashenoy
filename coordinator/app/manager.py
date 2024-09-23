from worker_nodes.app.celery_worker import celery_app
import uuid

# In-memory storage for jobs (this can be replaced with a database or Redis)
jobs_status = {}

def submit_eci_to_ecef(eci_trajectory):
    """Submit a job to convert ECI to ECEF"""
    job_id = str(uuid.uuid4())
    task = celery_app.send_task("worker_nodes.app.celery_tasks.ingest_eci_output_ecef", args=[job_id, eci_trajectory])
    jobs_status[job_id] = "pending"
    return task.id

def get_job_status(task_id):
    """Get the status of a job"""
    task = celery_app.AsyncResult(task_id)
    if task.state == 'PENDING':
        return {"status": "pending"}
    elif task.state == 'SUCCESS':
        return {"status": "completed", "result": task.result}
    elif task.state == 'FAILURE':
        return {"status": "failed", "error": str(task.info)}
    else:
        return {"status": task.state}

