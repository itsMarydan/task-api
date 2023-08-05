from fastapi import FastAPI
from pydantic import BaseModel

class ModelGetTask(BaseModel):
    id:int
    title:str
    description:str
    due_date:str
    completed:bool
    created_at:str
    created_by:str

class ModelPostTask(BaseModel):
    title:str
    description:str
    due_date:str
    completed:bool
    created_by:str

class ModelGetUser(BaseModel):
    id:int
    name:str
    email:str
    password:str

class ModelPostUser(BaseModel):
    name:str
    email:str
    password:str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks")
async def tasks()->list[ModelGetTask]:
    return [
        ModelGetTask(id=1, title="title", description="description", due_date="2021-01-01", completed=False, created_at="2021-01-01", created_by="user"),
        ModelGetTask(id=2, title="title", description="description", due_date="2021-01-01", completed=False, created_at="2021-01-01", created_by="user"),
        ModelGetTask(id=3, title="title", description="description", due_date="2021-01-01", completed=False, created_at="2021-01-01", created_by="user"),
        ModelGetTask(id=4, title="title", description="description", due_date="2021-01-01", completed=False, created_at="2021-01-01", created_by="user")
    ]

@app.get("/tasks/{task_id}")
async def task(task_id:int)->ModelGetTask:
    return ModelGetTask(id=task_id, title="title", description="description", due_date="2021-01-01", completed=False, created_at="2021-01-01", created_by="user")

@app.delete("/tasks/{task_id}")
async def task(task_id:int):
    return {"message": "delete_task", "param" : task_id}

@app.post("/tasks", status_code=201)
async def tasks(model:ModelPostTask) -> ModelPostTask:
    return ModelPostTask(title=model.title, description=model.description, due_date=model.due_date, completed=model.completed, created_by=model.created_by)

@app.put("/tasks")
async def tasks():
    return {"message": "put_task"}

@app.get("/users")
async def users()->list[ModelGetUser]:
    return [
        ModelGetUser(id=1, name="name", email="email", password="password"),
        ModelGetUser(id=2, name="name", email="email", password="password"),
    ]

@app.get("/users/{user_id}")
async def user(user_id:int)->ModelGetUser:
    return ModelGetUser(id=user_id, name="name", email="email", password="password")

@app.post("/users", status_code=201)
async def user(model):
    return {"message": "post_user", "object" : model}