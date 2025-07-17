import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import ollama
import json

from app.models.task import Task as DBTask, TaskCreate, TaskResponse
from app.models.project import Project as DBProject
from app.services.rag_service import RAGService
from app.core.config import settings
from app.core.db import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


def get_rag_service():
    return RAGService(
        ollama_api_url=settings.OLLAMA_API_URL, gemini_api_key=settings.GEMINI_API_KEY
    )


@router.post("/projects/{project_id}/tasks/generate", response_model=List[TaskResponse])
async def generate_tasks(
    project_id: str,
    objective: str,
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # 1. Query the RAG service to get relevant context
    context = rag_service.query(objective)

    # 2. Construct a prompt with the context and objective
    prompt = f"""
    Objective: {objective}

    Context:
    {context}

    Based on the objective and context, generate a list of tasks to complete the objective.
    Return the tasks as a JSON array of objects with the following keys: id, title, description.
    """

    # 3. Send the prompt to the LLM (Ollama)
    try:
        response = ollama.chat(
            model="gemma3:1b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a project manager. Your task is to break down an objective into a list of tasks. Return the tasks as a JSON array of objects with the following keys: id, title, description.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            format="json",
        )

        # 4. Parse the LLM response and create DB tasks
        tasks_json = json.loads(response["message"]["content"])
        tasks_data = [tasks_json] if "tasks" not in tasks_json else tasks_json["tasks"]

        created_tasks = []
        for task_data in tasks_data:
            db_task = DBTask(**task_data, project_id=project_id)
            db_task.id = str(uuid.uuid4())
            db.add(db_task)
            created_tasks.append(db_task)
        db.commit()
        for task in created_tasks:  # Refresh each task to get its ID
            db.refresh(task)

        return [TaskResponse.model_validate(task) for task in created_tasks]

    except ollama.ResponseError as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {e.error}")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse LLM response as JSON."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_all_tasks(project_id: str, db: Session = Depends(get_db)):
    tasks = db.query(DBTask).filter(DBTask.project_id == project_id).all()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(project_id: str, task_id: str, db: Session = Depends(get_db)):
    task = (
        db.query(DBTask)
        .filter(DBTask.project_id == project_id, DBTask.id == task_id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")
    return TaskResponse.model_validate(task)


@router.put("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: str,
    task_id: str,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = (
        db.query(DBTask)
        .join(DBProject)
        .filter(
            DBTask.project_id == project_id,
            DBTask.id == task_id,
            DBProject.user_id == current_user.id,
        )
        .first()
    )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    for key, value in task_update.model_dump().items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse.model_validate(db_task)


@router.delete(
    "/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = (
        db.query(DBTask)
        .join(DBProject)
        .filter(
            DBTask.project_id == project_id,
            DBTask.id == task_id,
            DBProject.user_id == current_user.id,
        )
        .first()
    )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    db.delete(db_task)
    db.commit()
    return
