from fastapi import APIRouter, Depends, Form
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.scheme.task import TaskResponse, TaskScheme
from src.repositories.task import TaskServices, get_task_service
from src.routes.user import get_payload

from typing import Annotated



router = APIRouter(tags=["tasks"], prefix='/api/tasks')


def get_user_id(token: dict =  Depends(get_payload)):
    
    user_id = int(token.get("sub"))
    if not user_id:
        raise HTTPException(status_code=400, detail="can't get user id")
    
    print(user_id)
    return user_id
    

def get_user_tasks(user_id: int = Depends(get_user_id), task_service: TaskServices = Depends(get_task_service)):
    tasks = task_service.get_tasks_by_user_id(user_id)

    if not tasks:
        raise HTTPException(status_code=400, detail="cant't get tasks")

    
    return tasks


@router.get("/")
def show_tasks(tasks: list[TaskResponse] = Depends(get_user_tasks)):
    
    
    tasks_info = []

    for task in tasks:
        tasks_info.append(
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "is_completed": task.is_completed,
            }
        )

    return tasks_info


def validate_task(task: TaskScheme = Form(...)): 
    
    return task


@router.post("/")
def add_task(user_id: int = Depends(get_user_id),
             task_data: TaskScheme=Depends(validate_task),
             task_service: TaskServices=Depends(get_task_service)):
        
        print(task_data)
        task_service.add_task(user_id=user_id, task_data=task_data)
