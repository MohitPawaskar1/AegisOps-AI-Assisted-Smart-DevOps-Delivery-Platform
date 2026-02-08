from fastapi import FastAPI
import uuid
from workers.job_worker import start_worker
from database.db import engine, Base
from models.job_model import Job


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "AegisOps Job Processor Running"}


from database.db import SessionLocal
from models.job_model import Job


@app.post("/jobs")
def create_job(task_name: str):

    db = SessionLocal()

    new_job = Job(task_name=task_name, status="pending")

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    db.close()

    return {"job_id": new_job.id, "status": new_job.status}



@app.get("/jobs/{job_id}")
def get_job(job_id: str):

    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    db.close()

    if job:
        return {"job_id": job.id, "status": job.status}

    return {"error": "Job not found"}
