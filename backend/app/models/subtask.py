import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="todo") # e.g., "todo", "done"
    task_id = Column(String(36), ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="subtasks")


# Pydantic models for request/response validation
from pydantic import BaseModel, ConfigDict


class SubtaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"


class SubtaskResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: str
    task_id: str

    model_config = ConfigDict(from_attributes=True)