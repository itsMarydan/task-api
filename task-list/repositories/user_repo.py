
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import Depends
from db import get_db
from models.models import UserEntity

class UserRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, search: str = ''):
        tasks = self.db.query(UserEntity) \
            .filter(or_(
            UserEntity.fname.contains(search),
            UserEntity.lname.contains(search))).all()

        return tasks

    def get_by_id(self, user_id: int):
        task = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        return task

    def create(self, task: any):
        new_task = UserEntity(**task.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update(self, user_id: int, task: any):
        existing_user = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not existing_user: return None

        # map the updated fields to the task object
        for k, v in task.dict().items(): setattr(existing_user, k, v)

        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user

    def delete(self, user_id: int):
        task = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not task: return None

        self.db.delete(task)
        self.db.commit()
        return task