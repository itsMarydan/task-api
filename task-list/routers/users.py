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
    return service.get_all(search)

# Get single user by id
@router.get("/users/{user_id}",response_model=schemas.UserSchema)
def get_user(user_id: int, service: UserService = Depends()):
    user = service.get_by_id(user_id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

# Create user
@router.post("/users", response_model=schemas.UserSchema)
def create_user(user: schemas.UserPostSchema, service: UserService = Depends()):
    return service.create(user)

# Update user
@router.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdateSchema, service: UserService = Depends()):
    existing_user = service.update(user_id, user)
    if not existing_user: raise HTTPException(status_code=404, detail="User not found")
    return existing_user

# Delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, user_service : UserService = Depends(), task_service : TaskService = Depends()):
    tasks = task_service.get_by_user_id(user_id)
    if tasks: raise HTTPException(status_code=400, detail="User has tasks and cannot be deleted")

    user = user_service.delete(user_id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user