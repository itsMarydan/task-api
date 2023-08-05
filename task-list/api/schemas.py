from pydantic import BaseModel
from datetime import datetime

class TaskSchema(BaseModel):
    title: str
    description: str
    completed: bool
    due_date: datetime
    created_by: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True