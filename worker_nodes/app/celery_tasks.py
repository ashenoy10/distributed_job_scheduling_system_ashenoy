from celery import Celery
import numpy as np
from celery import Celery
from .celery_worker import celery_app
from datetime import datetime
import math
from .worker_utils import update_worker_status

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# Constants
EARTH_ROTATION_RATE = 7.2921159e-5  # Earth's rotation rate in radians per second

def compute_era(timestamp: datetime) -> float:
    """
    Compute Earth Rotation Angle (ERA) based on the given timestamp.
    ERA = Earth's rotation rate * seconds since epoch
    """
    seconds_since_epoch = (timestamp - datetime(2000, 1, 1, 12, 0, 0)).total_seconds() # Approximate unix time
    era = (EARTH_ROTATION_RATE * seconds_since_epoch) % (2 * math.pi)  # In radians
    return era

def eci_to_ecef(eci_coords, timestamp):
    """
    Convert ECI coordinates to ECEF.
    
    eci_coords: Tuple (x, y, z) representing the ECI coordinates.
    timestamp: Datetime object for the time of the coordinates.
    
    Returns: Tuple (x_ecef, y_ecef, z_ecef)
    """
    x_eci, y_eci, z_eci = eci_coords
    era = compute_era(timestamp)

    # ECI to ECEF transformation matrix (inverse of ECEF to ECI)
    rotation_matrix = np.array([
        [np.cos(era), np.sin(era), 0],
        [-np.sin(era), np.cos(era), 0],
        [0, 0, 1]
    ])

    eci_vector = np.array([x_eci, y_eci, z_eci])
    ecef_vector = np.dot(rotation_matrix, eci_vector)
    return tuple(ecef_vector)

@celery_app.task(bind=True, name="worker_nodes.app.celery_tasks.ingest_eci_output_ecef")
def ingest_eci_output_ecef(self, job_id, eci_trajectory):
    """
    Ingests ECI trajectory and outputs ECEF trajectory.
    
    eci_trajectory: List of dictionaries with ECI coordinates and timestamps.
                    e.g., [{'x': ..., 'y': ..., 'z': ..., 'timestamp': 'YYYY-MM-DDTHH:MM:SS'}]
                    
    Returns a list of ECEF coordinates.
    """
    update_worker_status("busy", job_id)
    ecef_trajectory = []

    for point in eci_trajectory:
        eci_coords = (point['x'], point['y'], point['z'])
        timestamp = datetime.fromisoformat(point['timestamp'])
        
        # Convert each ECI point to ECEF
        ecef_coords = eci_to_ecef(eci_coords, timestamp)
        ecef_trajectory.append({
            'x_ecef': ecef_coords[0],
            'y_ecef': ecef_coords[1],
            'z_ecef': ecef_coords[2],
            'timestamp': point['timestamp']
        })
    update_worker_status("available")

    return {"job_id": job_id, "ecef_trajectory": ecef_trajectory}
