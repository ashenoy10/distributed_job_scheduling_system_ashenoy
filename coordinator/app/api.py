from fastapi import FastAPI, HTTPException
from .manager import submit_eci_to_ecef, get_job_status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ECIPoint(BaseModel):
    x: float
    y: float
    z: float
    timestamp: str  # ISO format: YYYY-MM-DDTHH:MM:SS

class ECIRequest(BaseModel):
    trajectory: List[ECIPoint]

@app.post("/submit-eci-to-ecef/")
def submit_eci_to_ecef_endpoint(eci_request: ECIRequest):
    try:
        task_id, job_id = submit_eci_to_ecef([dict(point) for point in eci_request.trajectory])
        return {"task_id": task_id, "job_id": job_id, "status": "Job submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job-status/{task_id}")
def job_status(task_id: str):
    status = get_job_status(task_id)
    if status:
        return status
    else:
        raise HTTPException(status_code=404, detail="Job not found")

# Define the expected data model
class WorkerStatus(BaseModel):
    worker_id: str
    status: str
    job_id: str

@app.post("/register-worker")
def register_worker(worker: WorkerStatus):
    reg_string = f"Worker registered: {worker.worker_id}, Status: {worker.status}"
    if worker.job_id != "":
        reg_string = reg_string + f", Job ID: {worker.job_id}"
    print(reg_string)
    return {"worker_id": worker.worker_id, "status": worker.status, "message": "Worker registered successfully"}
