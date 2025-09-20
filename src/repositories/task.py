from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database.dependency import get_db
from src.models.task import Task
from src.models.user import User
from src.scheme.task import TaskScheme, TaskUpdate


class TaskServices():

    def __init__(self, db: Session):
        self.db = db


    def get_max_task_id(self):
        max_id = self.db.query(func.max(Task.id)).scalar()
        return max_id or 0 

    def get_task_by_id(self, task_id: int):
        task = self.db.get(Task, task_id)
        return task 


    def add_task(self, user_id: int, task_data: TaskScheme):
        
        task_id = self.get_max_task_id()+1

        task = Task(
            id=task_id,
            name=task_data.name,
            description=task_data.description,
            is_completed=False,
            user_id=user_id,
        )

        self.db.add(task)
        self.db.commit()

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)

        if not task:
            return False

        self.db.delete(task)
        self.db.commit()

        return True


    def update_task(self, task_id: int, task_data: TaskUpdate):
        task = self.get_task_by_id(task_id)

        if not task:
            return False

        if task_data.name:
            task.name = task_data.name
        if task_data.description:
            task.description = task_data.description
        if task_data.is_completed:
            task.is_completed = task_data.is_completed

        self.db.commit()
        
        return True


    def get_user_tasks(self, user: User):
        tasks = user.tasks
        return tasks

    def get_tasks_by_user_id(self, user_id: int) -> list[Task]:
        tasks = (self.db.query(Task)
             .join(User.tasks)  
             .filter(User.id == user_id)
             .all())
    
        return tasks

def get_task_service(db: Session = Depends(get_db)):
    return TaskServices(db)