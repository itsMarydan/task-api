from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas import schemas
from log import log
from services.task_service import TaskService

# Initialize FastAPI app
router = APIRouter()

# Get all tasks
@router.get("/tasks", response_model=List[schemas.TaskSchema])
def get_tasks(service: TaskService = Depends(), search: str = ''):
    try:
        return service.get_all(search)
    except Exception as e:
        raise HTTPException(status_code=404, detail="problem loading tasks")

# Get single task by id
@router.get("/tasks/{task_id}",response_model=schemas.TaskSchema)
def get_task(task_id: int, service: TaskService = Depends()):
    try:
        return service.get_by_id(task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="problem loading task")

# Create task
@router.post("/tasks", response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskPostSchema, service: TaskService = Depends()):
    try:
        task = service.create(task)
        if not task : raise HTTPException(status_code=400, detail="User could not be created")
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem creating task")

# Update task
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskUpdateSchema, service: TaskService = Depends()):
    try:
        existing_task = service.update(task_id, task)
        if not existing_task: raise HTTPException(status_code=404, detail="Task not found")
        return existing_task
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem updating task")

# Delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, service : TaskService = Depends()):
    try:
        return service.delete(task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem deleting task")