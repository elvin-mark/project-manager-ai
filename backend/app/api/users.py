from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User as DBUser, UserResponse
from app.core.db import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user) # Requires authentication
):
    users = db.query(DBUser).all()
    return users
