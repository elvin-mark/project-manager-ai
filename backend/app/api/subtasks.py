import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.subtask import Subtask as DBSubtask, SubtaskCreate, SubtaskResponse
from app.models.task import Task as DBTask
from app.models.user import User as DBUser
from app.models.project import Project as DBProject
from app.core.db import get_db
from app.core.security import get_current_user
from app.services.llm_service import LlmException, AiService, get_llm_service
from app.models.requests.question import AskQuestionRequest

router = APIRouter()


@router.post(
    "/projects/{project_id}/tasks/{task_id}/subtasks/generate",
    response_model=List[SubtaskResponse],
)
async def generate_subtasks(
    project_id: str,
    task_id: str,
    objective: str,
    llm_service: AiService = Depends(get_llm_service),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = (
        db.query(DBTask)
        .filter(DBTask.id == task_id, DBTask.project_id == project_id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user not in task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to generate subtasks for this task"
        )

    # Construct a prompt for subtask generation
    prompt = f"""
    Given the following main task: "{task.title} - {task.description}"
    And the objective: "{objective}"

    Break down the objective into a list of smaller, actionable subtasks.
    Return the subtasks as a JSON array of objects with the following keys: title, description.
    """

    try:
        subtask_data_list = llm_service.get_tasks(
            prompt
        )  # Re-using get_tasks from LLM service

        created_subtasks = []
        for subtask_data in subtask_data_list:
            db_subtask = DBSubtask(**subtask_data, task_id=task_id)
            db_subtask.id = str(uuid.uuid4())
            db.add(db_subtask)
            created_subtasks.append(db_subtask)
        db.commit()
        for subtask in created_subtasks:
            db.refresh(subtask)

        return [SubtaskResponse.model_validate(subtask) for subtask in created_subtasks]

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


@router.get(
    "/projects/{project_id}/tasks/{task_id}/subtasks",
    response_model=List[SubtaskResponse],
)
def get_subtasks(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = (
        db.query(DBTask)
        .filter(DBTask.id == task_id, DBTask.project_id == project_id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user not in task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to view subtasks for this task"
        )

    subtasks = db.query(DBSubtask).filter(DBSubtask.task_id == task_id).all()
    return [SubtaskResponse.model_validate(subtask) for subtask in subtasks]


@router.put(
    "/projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}",
    response_model=SubtaskResponse,
)
def update_subtask(
    project_id: str,
    task_id: str,
    subtask_id: str,
    subtask_update: SubtaskCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    subtask = (
        db.query(DBSubtask)
        .filter(DBSubtask.id == subtask_id, DBSubtask.task_id == task_id)
        .first()
    )
    if subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")

    if current_user not in subtask.task.project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this subtask"
        )

    for key, value in subtask_update.model_dump(exclude_unset=True).items():
        setattr(subtask, key, value)

    db.add(subtask)
    db.commit()
    db.refresh(subtask)
    return SubtaskResponse.model_validate(subtask)


@router.post("/projects/{project_id}/tasks/{task_id}/subtasks/{subtask_id}/ask")
def ask_project_question(
    project_id: str,
    task_id: str,
    subtask_id: str,
    request: AskQuestionRequest,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
    llm_service: AiService = Depends(get_llm_service),
):
    db_subtask = (
        db.query(DBSubtask)
        .filter(DBSubtask.id == subtask_id, DBSubtask.task_id == task_id)
        .first()
    )
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")

    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user not in project.organization.members:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this project"
        )

    project_data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "assigned_to": task.assigned_to.username if task.assigned_to else None,
                "subtasks": [
                    {
                        "id": subtask.id,
                        "title": subtask.title,
                        "description": subtask.description,
                        "status": subtask.status,
                    }
                    for subtask in task.subtasks
                ],
            }
            for task in project.tasks
        ],
    }

    question = f"""Giving the following subtask:
    Title: {db_subtask.title}
    Description: {db_subtask.description}
    
    which belongs to the task:
    Title: {db_subtask.task.title}
    Description: {db_subtask.task.description}

    And the following comments under this task:
    {"\n".join([comment.content for comment in db_subtask.task.comments]) if db_subtask.task.comments else "None"}
    
    The user is asking the following question:
    {request.question}
    """

    answer = llm_service.ask_question(project_data, question)
    return {"answer": answer}
