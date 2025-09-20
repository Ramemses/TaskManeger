from pydantic import BaseModel
from typing import Optional



class TaskScheme(BaseModel):
    name: str
    description: str


class TaskUpdate(BaseModel):
    name: Optional[str] | None
    description: Optional[str] | None
    is_completed: Optional[str] | None


class TaskResponse(TaskScheme):
    id: int
    is_completed: bool

