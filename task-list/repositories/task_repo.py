
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_, insert, update, delete
from fastapi import Depends
from db import get_db
from log import log
from models.models import TaskEntity

class TaskRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, search: str = '', page: int = 1, limit: int = 100):
        tasks = self.db.query(TaskEntity) \
        .options(joinedload(TaskEntity.user)) \
        .filter(or_(
            TaskEntity.title.contains(search),
            TaskEntity.description.contains(search))).offset((page - 1) * limit).limit(limit).all()

        log.info(f"Tasks: {tasks}")
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

    def bulk_create(self, tasks_data, chunk_size=100):
        """
        :param tasks_data: List of dictionaries where each dictionary contains attributes for a task.
        :param chunk_size: Size of each batch to be inserted at once.
        :return: Success or failure of the bulk insert.
        """

        total_inserted = 0
        total_failed = 0

        for i in range(0, len(tasks_data), chunk_size):
            chunk = tasks_data[i:i + chunk_size]
            try:
                self.db.execute(
                    insert(TaskEntity),
                    chunk
                )
                self.db.commit()
                total_inserted += len(chunk)
                log.info(f"Inserted chunk {i // chunk_size + 1} successfully")
            except Exception as e:
                self.db.rollback()
                total_failed += len(chunk)
                log.error(f"Error occurred in chunk {i // chunk_size + 1}: {e}")

        if total_failed == 0:
            return {
                "status": True,
                "message": f"Insert completed with {total_inserted} successful inserts and {total_failed} failed "
                           f"inserts."
            }
        else:
            return {
                "status": False,
                "message": f"Insert completed with {total_inserted} successful inserts and {total_failed} failed "
            }

    def bulk_update(self, tasks_data, chunk_size=100):
        """
        :param tasks_data: List of dictionaries where each dictionary contains attributes for a task.
        :param chunk_size: Size of each batch to be updated at once.
        :return: Success or failure of the bulk update.
        """

        total_updated = 0
        total_failed = 0

        for i in range(0, len(tasks_data), chunk_size):
            chunk = tasks_data[i:i + chunk_size]
            try:
                self.db.execute(
                    update(TaskEntity),
                    chunk
                )
                self.db.commit()
                total_updated += len(chunk)
                log.info(f"Updated chunk {i // chunk_size + 1} successfully")
            except Exception as e:
                self.db.rollback()
                total_failed += len(chunk)
                log.error(f"Error occurred in chunk {i // chunk_size + 1}: {e}")

        if total_failed == 0:
            return {
                "status": True,
                "message": f"Update completed with {total_updated} successful updates and {total_failed} failed "
                           f"updates."
            }
        else:
            return {
                "status": False,
                "message": f"Update completed with {total_updated} successful updates and {total_failed} failed "
            }

    def bulk_delete(self, task_ids):
        try:
            stmt = delete(TaskEntity).where(TaskEntity.id.in_(task_ids))
            self.db.execute(stmt)
            self.db.commit()
            log.info(f"Deleted tasks: {task_ids}")
            return True
        except Exception as e:
            self.db.rollback()
            log.error(f"Error deleting tasks: {e}")
            return False

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

