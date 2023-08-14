from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from schemas import schemas
from models import models
from log import log
from db import get_db

# Initialize FastAPI app
router = APIRouter()

# Get all users
@router.get("/users")
def get_users(db: Session = Depends(get_db), search: str = ''):
    log.info("GET: users")
    users = db.query(models.UserEntity) \
        .filter(or_(
        models.UserEntity.fname.contains(search),
        models.UserEntity.lname.contains(search))).all()
    return users

# Get single user by id
@router.get("/users/{user_id}", response_model=schemas.UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")

    # an example of how to populate a field that is not in the database as long as the pydantic model has the field
    #return schemas.UserSchema(**user.__dict__, full_name=f"{user.fname} {user.lname}")
    return user


# Create user
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserPostSchema, db: Session = Depends(get_db)):
    new_user = models.UserEntity(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update user
@router.put("/users/{user_id}", status_code=status.HTTP_201_CREATED)
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
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    log.info("DELETE: users")
    tasks = db.query(models.TaskEntity).filter(models.TaskEntity.user_id == user_id).all()
    if len(tasks) > 0: raise HTTPException(status_code=400, detail="User has tasks and cannot be deleted")

    user = db.query(models.UserEntity).filter(models.UserEntity.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user