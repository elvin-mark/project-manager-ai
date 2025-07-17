from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str = "todo"
    subtasks: Optional[List["Task"]] = None
