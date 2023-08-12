from pydantic import BaseModel
from datetime import datetime
from typing import List

class TaskSchema(BaseModel):
    title: str
    description: str
    completed: bool
    due_date: datetime
    created_by: str
    user_id: int
    user: "UserSchema"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class UserSchema(BaseModel):
    fname: str
    lname: str
    tasks: List["TaskSchema"]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True