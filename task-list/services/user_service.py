from typing import List
from fastapi import Depends
from repositories.user_repo import UserRepo

class UserService:
    def __init__(self, user_repo: UserRepo  = Depends()):
        self.user_repo = user_repo

    def get_all(self, search: str = ''):
        return self.user_repo.get_all(search)

    def get_by_id(self, task_id: int):
        return self.user_repo.get_by_id(task_id)

    def create(self, task: any):
        return self.user_repo.create(task)

    def update(self, task_id: int, task: any):
        return self.user_repo.update(task_id, task)

    def delete(self, task_id: int):
        return self.user_repo.delete(task_id)