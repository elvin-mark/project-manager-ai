import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    name = Column(String, index=True)
    description = Column(String)
    organization_id = Column(String(36), ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


# Pydantic models for request/response validation
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str
    organization_id: str


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    organization_id: str

    model_config = ConfigDict(from_attributes=True)