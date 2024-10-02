import requests
import json
import os

def test_submit_job():
    # Submit a job to the coordinator
    response = requests.post(
        "http://localhost:8000/submit-eci-to-ecef/",
        json={"trajectory": [{"x": 7000.0, "y": 0.0, "z": 0.0, "timestamp": "2024-09-23T12:00:00"}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "Job submitted successfully"

    # Check job tracking by coordinator
    task_id = response.json()["task_id"]
    status_response = requests.get(f"http://localhost:8000/job-status/{task_id}")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert "status" in status_data
    assert status_data["status"] in ["pending", "completed", "failed"]

test_submit_job()

def test_worker_registration():
    # Check worker registration entry point
    response = requests.post("http://localhost:8000/register-worker", json={"worker_id": "worker_1", "status": "available", "job_id": ""})
    assert response.status_code == 200
    worker_status = response.json()
    assert worker_status["worker_id"] == "worker_1"
    assert worker_status["status"] == "available"
    assert worker_status["message"] == "Worker registered successfully"

test_worker_registration()

from concurrent.futures import ThreadPoolExecutor

def submit_job(trajectory_data):
    response = requests.post(
        "http://localhost:8000/submit-eci-to-ecef/",
        json=trajectory_data
    )
    return response.json()["task_id"]

def test_concurrent_jobs():

    trajectories = []

    # Open and read the JSON files
    for filename in [f'eci_trajectory_{num}.json' for num in range(1,6)]:
        with open(os.path.join(os.getcwd(),'tests','trajectories', filename), 'r') as file:
            data = json.load(file)
        trajectories.append(data)

    # Submit each trajectory 20 times, for a total of 100 submissions
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(submit_job, trajectory)
            for trajectory in trajectories
            for _ in range(20)  # Submit each trajectory 20 times
        ]

    task_ids = [future.result() for future in futures]

    # Check status for each job
    for task_id in task_ids:
        status_response = requests.get(f"http://localhost:8000/job-status/{task_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        print(f"task_id: {task_id}, status: {status_data['status']}")
        assert status_data["status"] in ["pending", "completed"]

test_concurrent_jobs()