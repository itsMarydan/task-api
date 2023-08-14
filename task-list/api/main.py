from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import datetime
from faker import Faker
import schemas, models
from typing import List
from log import log

from db import get_db, engine, Base

# Initialize FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return "Task API is running"

# Get all tasks
@app.get("/tasks", response_model=List[schemas.TaskSchema])
def get_tasks(db: Session = Depends(get_db), search: str = ''):
    tasks = db.query(models.TaskEntity) \
    .options(joinedload(models.TaskEntity.user)) \
    .filter(or_(
        models.TaskEntity.title.contains(search),
        models.TaskEntity.description.contains(search))).all()

    return tasks

# Get single task by id
@app.get("/tasks/{task_id}",response_model=schemas.TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db)):
    log.info("GET: tasks")
    task = db.query(models.TaskEntity) \
        .options(joinedload(models.TaskEntity.user)) \
        .filter(models.TaskEntity.id == task_id).first()

    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return task

# Create task
@app.post("/tasks", response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskPostSchema, db: Session = Depends(get_db)):
    log.info("POST: tasks")
    new_task = models.TaskEntity(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Update task
@app.put("/tasks/{task_id}")
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
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    log.info("DELETE: tasks")
    task = db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return task

############
## USERS ##
############

# Get all users
@app.get("/users")
def get_users(db: Session = Depends(get_db), search: str = ''):
    log.info("GET: users")
    users = db.query(models.UserEntity) \
        .filter(or_(
        models.UserEntity.fname.contains(search),
        models.UserEntity.lname.contains(search))).all()
    return users

# Get single user by id
@app.get("/users/{user_id}", response_model=schemas.UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")

    # an example of how to populate a field that is not in the database as long as the pydantic model has the field
    #return schemas.UserSchema(**user.__dict__, full_name=f"{user.fname} {user.lname}")
    return user


# Create user
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserPostSchema, db: Session = Depends(get_db)):
    new_user = models.UserEntity(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update user
@app.put("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def update_user(user_id: int, user: schemas.UserUpdateSchema, db: Session = Depends(get_db)):
    log.info("PUT: users")
    existing_user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not existing_user: raise HTTPException(status_code=404, detail="User not found")

    # map the updated fields to the user object
    for k, v in user.dict().items(): setattr(existing_user, k, v)

    db.commit()
    db.refresh(existing_user)
    return existing_user

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    log.info("DELETE: users")
    tasks = db.query(models.TaskEntity).filter(models.TaskEntity.user_id == user_id).all()
    if len(tasks) > 0: raise HTTPException(status_code=400, detail="User has tasks and cannot be deleted")

    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user


################################
## FOR TESTING PURPOSES ONLY ##
################################

# seed database with data
@app.get("/admin/seed/", status_code=status.HTTP_201_CREATED)
def seed_data(db: Session = Depends(get_db)):
    log.info("Seeding database")
    for i in range(1, 200):
        fake = Faker()

        u =  schemas.UserBaseSchema(fname=fake.first_name(), lname=fake.last_name())
        new_user = models.UserEntity(**u.dict())
        db.add(new_user)
        db.commit()

        t =  schemas.TaskPostSchema(user_id=new_user.id,title=fake.text(20), description=fake.text(), completed=False, due_date=datetime.datetime.now())
        new_task = models.TaskEntity(**t.dict())
        db.add(new_task)
        db.commit()
    return {"status": "seeded users and tasks"}

# clear database
@app.delete("/admin/delete/", status_code=status.HTTP_200_OK)
def delete_data(db: Session = Depends(get_db)):
    log.info("Deleting all data")
    db.query(models.TaskEntity).delete()
    db.query(models.UserEntity).delete()
    db.commit()
    return {"status": "deleted all tasks and users"}