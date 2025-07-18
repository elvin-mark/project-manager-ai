from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.task import Task as DBTask, TaskCreate, TaskResponse
from app.models.project import Project as DBProject
from app.core.db import get_db
from app.core.security import get_current_user
from app.models.user import (
    User as DBUser,
)
from app.services.llm_service import LlmException, AiService, get_llm_service

router = APIRouter()


@router.post("/projects/{project_id}/tasks/generate", response_model=List[TaskResponse])
async def generate_tasks(
    project_id: str,
    objective: str,
    due_date: datetime | None = None,
    llm_service: AiService = Depends(get_llm_service),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user not in project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to generate tasks for this project"
        )

    # 1. Query the RAG service to get relevant context (TODO)
    context = ""

    # 2. Construct a prompt with the context and objective
    prompt = f"""
    Objective: {objective}

    Context:
    {context}

    Based on the objective and context, generate a list of tasks to complete the objective.
    Return the tasks as a JSON array of objects with the following keys: id, title, description.
    """

    # 3. Send the prompt to the LLM and get the tasks
    try:
        task_data = llm_service.get_tasks(prompt)
        tasks_data = task_data

        created_tasks = []
        for task_data in tasks_data:
            db_task = DBTask(
                **task_data,
                project_id=project_id,
                assigned_user_id=current_user.id,
                due_date=due_date,
            )
            db_task.id = str(uuid.uuid4())
            db.add(db_task)
            created_tasks.append(db_task)
        db.commit()
        for task in created_tasks:  # Refresh each task to get its ID
            db.refresh(task)
            if task.assigned_to:
                task.assigned_username = task.assigned_to.username

        return [TaskResponse.model_validate(task) for task in created_tasks]

    except LlmException as e:
        raise HTTPException(status_code=500, detail=f"LLM API error: {e.message}")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse LLM response as JSON."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_all_tasks(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
    search_query: str | None = None,
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user not in project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to view tasks for this project"
        )

    query = db.query(DBTask).filter(DBTask.project_id == project_id)

    if search_query:
        query = query.filter(
            (DBTask.title.ilike(f"%{search_query}%"))
            | (DBTask.description.ilike(f"%{search_query}%"))
        )

    tasks = query.all()
    for task in tasks:
        if task.assigned_to:
            task.assigned_username = task.assigned_to.username
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
async def create_task(
    project_id: str,
    task_create: TaskCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user not in project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to create tasks for this project"
        )

    db_task = DBTask(
        id=str(uuid.uuid4()),
        project_id=project_id,
        title=task_create.title,
        description=task_create.description,
        due_date=task_create.due_date,
        status="todo",  # Default status for manually created tasks
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse.model_validate(db_task)


@router.get("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = (
        db.query(DBTask)
        .filter(DBTask.project_id == project_id, DBTask.id == task_id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    if current_user not in task.project.organization.members:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    if task.assigned_to:
        task.assigned_username = task.assigned_to.username
    return TaskResponse.model_validate(task)


@router.post(
    "/projects/{project_id}/tasks/{task_id}/assign", response_model=TaskResponse
)
def assign_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_task = (
        db.query(DBTask)
        .filter(DBTask.project_id == project_id, DBTask.id == task_id)
        .first()
    )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    if current_user not in db_task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to assign tasks in this project"
        )

    # Assign task to the current user
    db_task.assigned_user_id = current_user.id
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    if db_task.assigned_to:
        db_task.assigned_username = db_task.assigned_to.username
    return TaskResponse.model_validate(db_task)


@router.put("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: str,
    task_id: str,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_task = (
        db.query(DBTask)
        .filter(DBTask.project_id == project_id, DBTask.id == task_id)
        .first()
    )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    if current_user not in db_task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this task"
        )

    # Logic for reassigning task to self
    if (
        task_update.assigned_user_id == current_user.id
        and db_task.assigned_user_id != current_user.id
    ):
        # Ensure the current user is part of the organization
        if current_user not in db_task.project.organization.members:
            raise HTTPException(
                status_code=403,
                detail="Cannot assign task: User is not a member of this organization.",
            )
        db_task.assigned_user_id = current_user.id
    elif (
        task_update.assigned_user_id is not None
        and task_update.assigned_user_id != current_user.id
    ):
        # Allow unassigning or assigning to another user if current user has broader permissions (e.g., admin)
        # For now, only allow assigning to self or unassigning by anyone in the org
        # A more robust permission system would be needed here.
        if current_user not in db_task.project.organization.members:  # Basic check
            raise HTTPException(
                status_code=403, detail="Not authorized to assign task to other users."
            )

        # Verify the assigned user is also in the same organization
        assigned_user = (
            db.query(DBUser).filter(DBUser.id == task_update.assigned_user_id).first()
        )
        if (
            not assigned_user
            or assigned_user not in db_task.project.organization.members
        ):
            raise HTTPException(
                status_code=400,
                detail="Assigned user is not a member of this organization.",
            )

        db_task.assigned_user_id = task_update.assigned_user_id
    elif task_update.assigned_user_id is None:
        db_task.assigned_user_id = None

    for key, value in task_update.model_dump(exclude_unset=True).items():
        if key not in [
            "assigned_user_id",
            "due_date",
        ]:  # assigned_user_id and due_date are handled above
            setattr(db_task, key, value)
    if task_update.due_date is not None:
        db_task.due_date = task_update.due_date

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    if db_task.assigned_to:
        db_task.assigned_username = db_task.assigned_to.username
    return TaskResponse.model_validate(db_task)


@router.delete(
    "/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_task = (
        db.query(DBTask)
        .filter(DBTask.project_id == project_id, DBTask.id == task_id)
        .first()
    )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    if current_user not in db_task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this task"
        )

    db.delete(db_task)
    db.commit()
    return
