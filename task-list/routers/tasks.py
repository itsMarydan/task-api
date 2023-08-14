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
    return service.get_all(search)

# Get single task by id
@router.get("/tasks/{task_id}",response_model=schemas.TaskSchema)
def get_task(task_id: int, service: TaskService = Depends()):
    task = service.get_by_id(task_id)
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return task

# Create task
@router.post("/tasks", response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskPostSchema, service: TaskService = Depends()):
    return service.create(task)

# Update task
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskUpdateSchema, service: TaskService = Depends()):
    existing_task = service.update(task_id, task)
    if not existing_task: raise HTTPException(status_code=404, detail="Task not found")
    return existing_task

# Delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, service : TaskService = Depends()):
    task = service.delete(task_id)
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return task