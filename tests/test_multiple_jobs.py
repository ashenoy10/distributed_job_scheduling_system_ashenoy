import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

# Sample trajectory data
data = {
    "trajectory": [
        {"x": 7000.0, "y": 0.0, "z": 0.0, "timestamp": "2024-09-23T12:00:00"},
        {"x": 0.0, "y": 7000.0, "z": 0.0, "timestamp": "2024-09-23T12:00:10"},
        {"x": 0.0, "y": 0.0, "z": 7000.0, "timestamp": "2024-09-23T12:00:20"}
    ]
}

# Function to submit a job
def submit_job():
    url = "http://localhost:8000/submit-eci-to-ecef/"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Submit multiple jobs concurrently
def submit_multiple_jobs(n_jobs):
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(submit_job) for _ in range(n_jobs)]
        for future in futures:
            print(future.result())
    return futures

def check_status(job_id):
    url = f"http://localhost:8000/job-status/{job_id}"
    response = requests.get(url)
    print(response.json())
    return response.json()

# Submit 10 jobs concurrently
futures = submit_multiple_jobs(10)
time.sleep(5)
for future in futures:
    task_id = future.result()['task_id']
    check_status(task_id)
