from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserBaseSchema(BaseModel):
    fname: str
    lname: str

    class Config:
        orm_mode = True

class UserSchema(UserBaseSchema):
    id: int

class UserPostSchema(UserBaseSchema):
    fname: str
    lname: str

class UserUpdateSchema(UserBaseSchema):
    fname: str
    lname: str

class TaskBaseSchema(BaseModel):
    title: str
    description: str
    completed: bool
    due_date: datetime

    class Config:
        orm_mode = True

class TaskSchema(TaskBaseSchema):
    id: int
    title: str
    description: str
    completed: bool
    due_date: datetime
    user_id: int
    user: 'UserSchema'

class TaskPostSchema(TaskBaseSchema):
    title: str
    description: str
    completed: bool
    due_date: datetime
    user_id: int

class TaskUpdateSchema(TaskBaseSchema):
    title: str
    description: str
    completed: bool
    due_date: datetime