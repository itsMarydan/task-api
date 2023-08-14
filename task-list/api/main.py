import csv
import json
from io import StringIO

from fastapi import FastAPI, status, UploadFile, HTTPException

from api.db import SessionLocal
from api.helpers.log import log
from api.helpers.procees_data import process_csv
from api.schemas import TaskSchema, BulkDeleteData
from api.service.task_service import TaskService

# Initialize FastAPI app
app = FastAPI()


# Create the database tables
# Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    log.info("Starting up")
    log.info("Creating tables")
    ## TODO

    csv_file = open('tasks.csv', 'r')
    tasks = list(csv.DictReader(csv_file))
    data = process_csv(tasks)
    session = SessionLocal()
    try:
        service = TaskService(session)
        service.bulk_create(data)
        log.info("Created tables")
    except Exception as e:
        log.error(f"Error creating tables: {e}")
        session.rollback()
    finally:
        session.close()




@app.get("/")
def root():
    return "Task API is running"


# Get all tasks
# @app.get("/tasks")
# def get_tasks(db: Session = Depends(get_db), search: str = ''):
#     tasks = db.query(TaskEntity).filter(or_(
#         TaskEntity.title.contains(search),
#         TaskEntity.description.contains(search))).all()
#     return {"status": "success", "task": tasks}


@app.get("/tasks")
def get_tasks():
    log.info("Starting session")
    session = SessionLocal()
    service = TaskService(session)
    try:
        tasks = service.get_all()
        return {"status": "success", "task": tasks}
    except Exception as e:
        log.error(f"Error getting tasks: {e}")
        return {"status": "error", "message": "Error getting tasks"}
    finally:
        log.info("Closing session")
        session.close()


# Get single task by id
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    session = SessionLocal()
    service = TaskService(session)
    try:
        task = service.get(task_id)
        if task is None:
            return {"status": "error", "message": "Task not found"}
        return {"status": "success", "task": task}
    except Exception as e:
        log.error(f"Error getting task: {e}")
        return {"status": "error", "message": "Error getting task"}
    finally:
        session.close()


# Create task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskSchema):
    session = SessionLocal()
    service = TaskService(session)
    log.info(f"Creating task: {task}")
    data = task.model_dump()
    try:
        new_task = service.create(data)
        if new_task is None:
            raise HTTPException(status_code=400, detail="Error creating task")
        return {"status": "success", "task": new_task}
    except Exception as e:
        log.error(f"Error creating task: {e}")
        return {"status": "error", "message": "Error creating task"}
    finally:
        session.close()


# Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskSchema):
    session = SessionLocal()
    service = TaskService(session)
    log.info(f"Updating task: {task}")
    data = task.model_dump()
    try:
        find_task = service.get(task_id)
        if find_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        updated_task = service.update(task_id, data)
        if updated_task is False:
            raise HTTPException(status_code=400, detail="Error updating task")
        return {"status": "success", "task": "Task updated successfully"}
    except Exception as e:
        log.error(f"Error updating task: {e}")
        return {"status": "error", "message": "Error updating task"}
    finally:
        session.close()


# Delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    session = SessionLocal()
    service = TaskService(session)
    log.info(f"Deleting task: {task_id}")
    try:
        find_task = service.get(task_id)
        if find_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        deleted_task = service.delete(task_id)
        if deleted_task is False:
            raise HTTPException(status_code=400, detail="Error deleting task")
        return {"status": "success", "task": "Task deleted successfully"}
    except Exception as e:
        log.error(f"Error deleting task: {e}")
        return {"status": "error", "message": "Error deleting task"}
    finally:
        session.close()


# Bulk create tasks

@app.post("/tasks/bulk")
async def bulk_create_tasks(file: UploadFile):
    session = SessionLocal()
    service = TaskService(session)
    log.info(f"File name: {file.filename}")
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
        result = service.bulk_create(data)
        log.info(f"Result: {result}")
        if result['status']:
            log.info(f"Message: {result['message']}")
            return {"status": "success", "response": result['message']}
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


# Bulk update tasks

@app.patch("/tasks/bulk")
async def bulk_update_tasks(file: UploadFile):
    session = SessionLocal()
    service = TaskService(session)
    log.info(f"File name: {file.filename}")
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
    finally:
        session.close()


# Bulk delete tasks

@app.delete("/tasks/bulk")
async def bulk_delete_tasks(data: BulkDeleteData):
    session = SessionLocal()
    service = TaskService(session)
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
    finally:
        session.close()


################################
## FOR TESTING PURPOSES ONLY ##
################################

# # seed database with tasks
# @app.get("/tasks/seed/", status_code=status.HTTP_201_CREATED)
# def seed_task(db: Session = Depends(get_db)):
#     for i in range(1, 200):
#         fake = Faker()
#         t = TaskSchema(title=fake.text(20), description=fake.text(), completed=False, due_date=datetime.datetime.now(),
#                        created_by=fake.name())
#         print(t)
#         new_task = TaskEntity(**t.dict())
#         db.add(new_task)
#         db.commit()
#     return {"status": "seeded tasks"}


# clear database
@app.delete("/tasks/delete", status_code=status.HTTP_200_OK)
def seed_task():
    session = SessionLocal()
    service = TaskService(session)
    service.delete_all()
    return {"status": "deleted all tasks"}
