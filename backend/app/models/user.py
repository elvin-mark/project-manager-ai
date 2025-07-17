import uuid
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base
from pydantic import BaseModel, ConfigDict

# Association table for User-Organization many-to-many relationship
user_organization_association = Table(
    "user_organization_association",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("organization_id", String(36), ForeignKey("organizations.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # projects = relationship("Project", back_populates="owner") # Removed as projects no longer belong to users directly
    organizations = relationship("Organization", secondary=user_organization_association, back_populates="members")
    assigned_tasks = relationship("Task", back_populates="assigned_to")

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
