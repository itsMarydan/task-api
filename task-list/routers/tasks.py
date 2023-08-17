import csv
import json
from io import StringIO

from fastapi import APIRouter, HTTPException, Depends, UploadFile, Request, File
from typing import List

from helper import process_csv
from schemas import schemas
from log import log
from schemas.schemas import BulkDeleteData
from services.task_service import TaskService

# Initialize FastAPI app
router = APIRouter()


# Get all tasks
@router.get("/tasks", response_model=List[schemas.TaskSchema])
def get_tasks(service: TaskService = Depends(), search: str = '', page: int = 1, limit: int = 100):
    try:
        return service.get_all(search, page, limit)
    except Exception as e:
        log.error(f"Error occurred: {e}")
        raise HTTPException(status_code=404, detail="problem loading tasks")


# Get single task by id
@router.get("/tasks/{task_id}", response_model=schemas.TaskSchema)
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
        if not task: raise HTTPException(status_code=400, detail="User could not be created")
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem creating task")


@router.post("/tasks/bulk")
async def create_bulk_tasks(file: UploadFile = File(...), service: TaskService = Depends()):
    try:
        if file.filename.endswith('.csv'):
            contents = await file.read()
            contents_string = contents.decode("utf-8")
            csv_file = StringIO(contents_string)
            tasks = list(csv.DictReader(csv_file))
            data = process_csv(tasks)
            log.info(f"Data from csv: {data}")
        elif file.filename.endswith('.json'):
            contents = await file.read()
            data = json.loads(contents)
            log.info(f"Data from json: {data}")
        else:
            raise HTTPException(status_code=400, detail="File type not supported")

        result = service.bulk_create(data)
        log.info(f"Result from bulk create: {result}")
        if result['status']:
            log.info(f"Message: {result['message']}")
            return {"status": "success", "response": result['message']}
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except Exception as e:
        log.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/tasks/bulk")
async def bulk_update_tasks(file: UploadFile = File(...), service: TaskService = Depends()):
    try:
        if file.filename.endswith('.json'):
            contents = await file.read()
            data = json.loads(contents)
            log.info(f"Data from json: {data}")
        elif file.filename.endswith('.csv'):
            contents = await file.read()
            contents_string = contents.decode("utf-8")
            csv_file = StringIO(contents_string)
            tasks = list(csv.DictReader(csv_file))
            data = process_csv(tasks)
            log.info(f"Data from csv: {data}")
        else:
            raise HTTPException(status_code=400, detail="File type not supported")
        result = service.bulk_update(data)
        log.info(f"Result: {result}")
        if result['status']:
            log.info(f"Message: {result['message']}")
            return {"status": "success", "response": result['message']}
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/tasks/bulk")
async def bulk_delete_tasks(data: BulkDeleteData, service: TaskService = Depends()):
    data = data.data
    try:
        result = service.bulk_delete(data)
        log.info(f"Result: {result}")
        if result:
            log.info(f"Message: {result}")
            return {"status": "success", "response": result}
        else:
            raise HTTPException(status_code=400, detail=result)
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


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
def delete_task(task_id: int, service: TaskService = Depends()):
    try:
        return service.delete(task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem deleting task")
