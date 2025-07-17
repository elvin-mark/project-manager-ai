from fastapi import APIRouter, Depends, HTTPException
from typing import List
import ollama
import json

from app.models.task import Task
from app.services.rag_service import RAGService
from app.core.config import settings

router = APIRouter()


def get_rag_service():
    return RAGService(
        ollama_api_url=settings.OLLAMA_API_URL, gemini_api_key=settings.GEMINI_API_KEY
    )


@router.post("/tasks/generate", response_model=List[Task])
async def generate_tasks(
    objective: str,
    rag_service: RAGService = Depends(get_rag_service),
):
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

        # 4. Parse the LLM response and return the tasks
        tasks_json = json.loads(response["message"]["content"])
        tasks = [tasks_json] if "tasks" not in tasks_json else tasks_json["tasks"]
        return [Task(**task) for task in tasks]

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
