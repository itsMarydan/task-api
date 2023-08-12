from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
import datetime
from faker import Faker
import schemas, models
from sqlalchemy.orm import Load, joinedload

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
    task.user
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

############
## USERS ##
############

# Get all users
@app.get("/users")
def get_users(db: Session = Depends(get_db), search: str = ''):
    users = db.query(models.UserEntity).filter(or_(
        models.UserEntity.fname.contains(search),
        models.UserEntity.lname.contains(search))).all()
    return {"status": "success", "user": users}

# Get single user by id
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    user.tasks
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "user": user}

# Create user
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    new_user = models.UserEntity(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "user": new_user}

# Update user
@app.put("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def update_user(user_id: int, user: schemas.UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not existing_user: raise HTTPException(status_code=404, detail="User not found")

    # map the updated fields to the user object
    for k, v in user.dict().items(): setattr(existing_user, k, v)

    db.commit()
    db.refresh(existing_user)
    return {"status": "success", "user": existing_user}

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"status": "success", "user": user}


################################
## FOR TESTING PURPOSES ONLY ##
################################

# seed database with data
@app.get("/admin/seed/", status_code=status.HTTP_201_CREATED)
def seed_data(db: Session = Depends(get_db)):
    for i in range(1, 200):
        fake = Faker()

        u =  schemas.UserSchema(fname=fake.first_name(), lname=fake.last_name())
        new_user = models.UserEntity(**u.dict())
        db.add(new_user)
        db.commit()

        t =  schemas.TaskSchema(user_id=new_user.id,title=fake.text(20), description=fake.text(), completed=False, due_date=datetime.datetime.now() , created_by=fake.name())
        new_task = models.TaskEntity(**t.dict())
        db.add(new_task)
        db.commit()
    return {"status": "seeded users and tasks"}

# clear database
@app.delete("/admin/delete/", status_code=status.HTTP_200_OK)
def delete_data(db: Session = Depends(get_db)):
    db.query(models.TaskEntity).delete()
    db.query(models.UserEntity).delete()
    db.commit()
    return {"status": "deleted all tasks and users"}