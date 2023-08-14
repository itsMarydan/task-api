from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List
from schemas import schemas
from models import models
from log import log
from db import get_db


# Initialize FastAPI app
router = APIRouter()

# Get all tasks
@router.get("/tasks", response_model=List[schemas.TaskSchema])
def get_tasks(db: Session = Depends(get_db), search: str = ''):
    tasks = db.query(models.TaskEntity) \
    .options(joinedload(models.TaskEntity.user)) \
    .filter(or_(
        models.TaskEntity.title.contains(search),
        models.TaskEntity.description.contains(search))).all()

    return tasks

# Get single task by id
@router.get("/tasks/{task_id}",response_model=schemas.TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db)):
    log.info("GET: tasks")
    task = db.query(models.TaskEntity) \
        .options(joinedload(models.TaskEntity.user)) \
        .filter(models.TaskEntity.id == task_id).first()

    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return task

# Create task
@router.post("/tasks", response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskPostSchema, db: Session = Depends(get_db)):
    log.info("POST: tasks")
    new_task = models.TaskEntity(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Update task
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskUpdateSchema, db: Session = Depends(get_db)):
    log.info("PUT: tasks")
    existing_task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not existing_task: raise HTTPException(status_code=404, detail="Task not found")

    # map the updated fields to the task object
    for k, v in task.dict().items(): setattr(existing_task, k, v)

    db.commit()
    db.refresh(existing_task)
    return existing_task

# Delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    log.info("DELETE: tasks")
    task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return task
