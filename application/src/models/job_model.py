from sqlalchemy import Column, String
import uuid

from database.db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_name = Column(String)
    status = Column(String)
