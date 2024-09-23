from fastapi import FastAPI, HTTPException
from app.manager import submit_job, get_job_status
from pydantic import BaseModel

app = FastAPI()

class JobRequest(BaseModel):
    data: str  # Job-specific data; modify as needed

@app.post("/submit-job/")
def submit_job_endpoint(job: JobRequest):
    try:
        job_id = submit_job(job.data)
        return {"job_id": job_id, "status": "Job submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    status = get_job_status(job_id)
    if status:
        return {"job_id": job_id, "status": status}
    else:
        raise HTTPException(status_code=404, detail="Job not found")
