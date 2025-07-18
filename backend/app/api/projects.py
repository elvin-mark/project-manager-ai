from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.project import Project as DBProject, ProjectCreate, ProjectResponse
from app.models.user import User as DBUser
from app.models.organization import Organization as DBOrganization
from app.models.task import Task as DBTask
from app.core.db import get_db
from app.core.security import get_current_user
from pydantic import BaseModel

router = APIRouter()


@router.post(
    "/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == project.organization_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to create projects in this organization")

    db_project = DBProject(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/organizations/{org_id}/projects", response_model=List[ProjectResponse])
def get_all_projects(
    org_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == org_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to view projects in this organization")

    projects = (
        db.query(DBProject)
        .filter(DBProject.organization_id == org_id)
        .all()
    )
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    project = (
        db.query(DBProject)
        .filter(DBProject.id == project_id)
        .first()
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if the current user is a member of the project's organization
    if current_user not in project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")

    return project


class ProjectSummaryResponse(BaseModel):
    total_tasks: int
    todo_tasks: int
    in_progress_tasks: int
    done_tasks: int


@router.get("/projects/{project_id}/summary", response_model=ProjectSummaryResponse)
def get_project_summary(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user not in project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to view this project summary")

    total_tasks = db.query(DBTask).filter(DBTask.project_id == project_id).count()
    todo_tasks = db.query(DBTask).filter(DBTask.project_id == project_id, DBTask.status == "todo").count()
    in_progress_tasks = db.query(DBTask).filter(DBTask.project_id == project_id, DBTask.status == "in_progress").count()
    done_tasks = db.query(DBTask).filter(DBTask.project_id == project_id, DBTask.status == "done").count()

    return ProjectSummaryResponse(
        total_tasks=total_tasks,
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        done_tasks=done_tasks,
    )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_project = (
        db.query(DBProject)
        .filter(DBProject.id == project_id)
        .first()
    )
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if the current user is a member of the project's organization
    if current_user not in db_project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    db.delete(db_project)
    db.commit()
    return