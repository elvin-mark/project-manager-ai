import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.db import Base
from pydantic import BaseModel, ConfigDict

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    projects = relationship("Project", back_populates="organization")
    members = relationship("User", secondary="user_organization_association", back_populates="organizations")

class OrganizationCreate(BaseModel):
    name: str
    description: str | None = None

class OrganizationResponse(BaseModel):
    id: str
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
