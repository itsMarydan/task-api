
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import Depends
from db import get_db
from models.models import UserEntity

class UserRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, search: str = ''):
        users = self.db.query(UserEntity) \
            .filter(or_(
            UserEntity.fname.contains(search),
            UserEntity.lname.contains(search))).all()

        return users

    def get_by_id(self, user_id: int):
        user = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        return user

    def create(self, user: any):
        new_user = UserEntity(**user.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update(self, user_id: int, user: any):
        existing_user = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not existing_user: return None

        # map the updated fields to the user object
        for k, v in user.dict().items(): setattr(existing_user, k, v)

        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user

    def delete(self, user_id: int):
        user = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not user: return None

        self.db.delete(user)
        self.db.commit()
        return user