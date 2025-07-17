import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="todo")
    project_id = Column(String, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="tasks")


# Pydantic model for request/response validation
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str = "todo"


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    project_id: str

    model_config = ConfigDict(from_attributes=True)
