from fastapi import FastAPI
from db import engine
from routers import users, tasks, admin

# Initialize FastAPI app
app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Hello!"}

# Create the database tables
from models.models import Base
Base.metadata.create_all(bind=engine)