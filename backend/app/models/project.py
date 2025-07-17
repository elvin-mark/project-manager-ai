import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    name = Column(String, index=True)
    description = Column(String)

    tasks = relationship("Task", back_populates="project")


# Pydantic models for request/response validation
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
