import uuid
from sqlalchemy import Column, String, ForeignKey
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
    assigned_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")
    assigned_to = relationship("User", back_populates="assigned_tasks")


# Pydantic model for request/response validation
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str = "todo"
    assigned_user_id: str | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    project_id: str
    assigned_user_id: str | None = None
    assigned_username: str | None = None # For display purposes

    model_config = ConfigDict(from_attributes=True)