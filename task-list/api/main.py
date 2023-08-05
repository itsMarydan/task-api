from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
import datetime
from faker import Faker
import schemas, models

from db import get_db, engine, Base

# Initialize FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return "Task API is running"

# Get all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db), search: str = ''):
    tasks = db.query(models.TaskEntity).filter(or_(
        models.TaskEntity.title.contains(search),
        models.TaskEntity.description.contains(search))).all()
    return {"status": "success", "task": tasks}

# Get single task by id
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success", "task": task}

# Create task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskSchema, db: Session = Depends(get_db)):
    new_task = models.TaskEntity(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status": "success", "task": new_task}

# Update task
@app.put("/tasks/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(task_id: int, task: schemas.TaskSchema, db: Session = Depends(get_db)):
    existing_task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not existing_task: raise HTTPException(status_code=404, detail="Task not found")

    # map the updated fields to the task object
    for k, v in task.dict().items(): setattr(existing_task, k, v)

    db.commit()
    db.refresh(existing_task)
    return {"status": "success", "task": existing_task}

# Delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"status": "success", "task": task}


################################
## FOR TESTING PURPOSES ONLY ##
################################

# seed database with tasks
@app.get("/tasks/seed/", status_code=status.HTTP_201_CREATED)
def seed_task(db: Session = Depends(get_db)):
    for i in range(1, 200):
        fake = Faker()
        t =  schemas.TaskSchema(title=fake.text(20), description=fake.text(), completed=False, due_date=datetime.datetime.now() , created_by=fake.name())
        new_task = models.TaskEntity(**t.dict())
        db.add(new_task)
        db.commit()
    return {"status": "seeded tasks"}

# clear database
@app.delete("/tasks/delete/", status_code=status.HTTP_200_OK)
def seed_task(db: Session = Depends(get_db)):
    db.query(models.TaskEntity).delete()
    db.commit()
    return {"status": "deleted all tasks"}