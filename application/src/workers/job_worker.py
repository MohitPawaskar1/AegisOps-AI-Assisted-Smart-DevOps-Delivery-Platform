import time
import threading

from database.db import SessionLocal
from models.job_model import Job


def process_jobs():

    while True:

        db = SessionLocal()

        pending_jobs = db.query(Job).filter(Job.status == "pending").all()

        for job in pending_jobs:

            print(f"Processing job {job.id}")

            job.status = "processing"
            db.commit()

            time.sleep(5)

            job.status = "completed"
            db.commit()

            print(f"Completed job {job.id}")

        db.close()
        time.sleep(2)


def start_worker():
    worker_thread = threading.Thread(target=process_jobs)
    worker_thread.daemon = True
    worker_thread.start()
