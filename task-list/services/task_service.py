from typing import List
from fastapi import Depends
from repositories.task_repo import TaskRepo

class TaskService:
    def __init__(self, task_repo: TaskRepo  = Depends()):
        self.task_repo = task_repo

    def get_all(self, search: str = ''):
        return self.task_repo.get_all(search)

    def get_by_id(self, task_id: int):
        return self.task_repo.get_by_id(task_id)

    def get_by_user_id(self, user_id: int):
        return self.task_repo.get_by_user_id(user_id)

    def create(self, task: any):
        return self.task_repo.create(task)

    def update(self, task_id: int, task: any):
        return self.task_repo.update(task_id, task)

    def delete(self, task_id: int):
        return self.task_repo.delete(task_id)