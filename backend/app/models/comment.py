import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    task_id = Column(String(36), ForeignKey("tasks.id"))
    user_id = Column(String(36), ForeignKey("users.id"))

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")


# Pydantic models for request/response validation
from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    task_id: str
    user_id: str
    username: str | None = None # For display purposes

    model_config = ConfigDict(from_attributes=True)