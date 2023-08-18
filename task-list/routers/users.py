from fastapi import APIRouter, HTTPException, Depends, status
from schemas import schemas
from models import models
from log import log
from services.user_service import UserService
from services.task_service import TaskService

from typing import List

# Initialize FastAPI app
router = APIRouter()

# Initialize FastAPI app
router = APIRouter()

# Get all users
@router.get("/users", response_model=List[schemas.UserSchema])
def get_users(service: UserService = Depends(), search: str = ''):
    users = service.get_all(search)
    return users

# Get single user by id
@router.get("/users/{user_id}",response_model=schemas.UserSchema)
def get_user(user_id: int, service: UserService = Depends()):
    try:
        return service.get_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="problem loading user")

# Create user
@router.post("/users", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserPostSchema, service: UserService = Depends()):
    try:
        user = service.create(user)
        if not user : raise HTTPException(status_code=400, detail="User could not be created")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem creating user")

# Update user
@router.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdateSchema, service: UserService = Depends()):
    try:
        existing_user = service.update(user_id, user)
        if not existing_user: raise HTTPException(status_code=404, detail="User not found")
        return existing_user
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem updating user")

# Delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, user_service : UserService = Depends(), task_service : TaskService = Depends()):
    try:
        tasks = task_service.get_by_user_id(user_id)
        if tasks: return {"message": "User has tasks and cannot be delete"}
        return user_service.delete(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="problem deleting user")


