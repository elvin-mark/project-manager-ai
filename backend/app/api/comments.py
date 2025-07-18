from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.comment import Comment as DBComment, CommentCreate, CommentResponse
from app.models.task import Task as DBTask
from app.models.user import User as DBUser
from app.core.db import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.post("/projects/{project_id}/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    project_id: str,
    task_id: str,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = db.query(DBTask).filter(DBTask.id == task_id, DBTask.project_id == project_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user not in task.project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to comment on this task")

    db_comment = DBComment(**comment.model_dump(), task_id=task_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    db_comment.username = current_user.username
    return CommentResponse.model_validate(db_comment)


@router.get("/projects/{project_id}/tasks/{task_id}/comments", response_model=List[CommentResponse])
def get_comments(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = db.query(DBTask).filter(DBTask.id == task_id, DBTask.project_id == project_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user not in task.project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to view comments for this task")

    comments = db.query(DBComment).filter(DBComment.task_id == task_id).order_by(DBComment.created_at).all()
    for comment in comments:
        if comment.user:
            comment.username = comment.user.username
    return [CommentResponse.model_validate(comment) for comment in comments]