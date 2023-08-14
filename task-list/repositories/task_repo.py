
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_
from fastapi import Depends
from db import get_db
from models.models import TaskEntity

class TaskRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, search: str = ''):
        tasks = self.db.query(TaskEntity) \
        .options(joinedload(TaskEntity.user)) \
        .filter(or_(
            TaskEntity.title.contains(search),
            TaskEntity.description.contains(search))).all()
        return tasks

    def get_by_id(self, task_id: int):
        task = self.db.query(TaskEntity) \
        .options(joinedload(TaskEntity.user)) \
        .filter(TaskEntity.id == task_id).first()
        return task

    def get_by_user_id(self, user_id: int):
        tasks = self.db.query(TaskEntity) \
        .options(joinedload(TaskEntity.user)) \
        .filter(TaskEntity.user_id == user_id).all()
        return tasks

    def create(self, task: any):
        new_task = TaskEntity(**task.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update(self, task_id: int, task: any):
        existing_task = self.db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if not existing_task: return None

        # map the updated fields to the task object
        for k, v in task.dict().items(): setattr(existing_task, k, v)

        self.db.commit()
        self.db.refresh(existing_task)
        return existing_task

    def delete(self, task_id: int):
        task = self.db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if not task: return None

        self.db.delete(task)
        self.db.commit()
        return task