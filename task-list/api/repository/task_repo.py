from api.models import TaskEntity
from api.helpers.log import log
from sqlalchemy import update, insert, delete


class TaskRepo:

    def __init__(self, session):
        self.session = session

    def create(self, data):
        new_task = TaskEntity(**data)
        try:
            self.session.add(new_task)
            self.session.commit()
            log.info(f"Created task: {new_task}")
            return data
        except Exception as e:
            self.session.rollback()
            log.error(f"Error creating task: {e}")
            return None

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
                self.session.execute(
                    insert(TaskEntity),
                    chunk
                )
                self.session.commit()
                total_inserted += len(chunk)
                log.info(f"Inserted chunk {i // chunk_size + 1} successfully")
            except Exception as e:
                self.session.rollback()
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

    def get(self, task_id):
        try:
            task = self.session.query(TaskEntity).get(task_id)
            return task
        except Exception as e:
            log.error(f"Error getting task: {e}")
            return None

    def get_all(self):
        try:
            tasks = self.session.query(TaskEntity).all()
            return tasks
        except Exception as e:
            log.error(f"Error getting tasks: {e}")
            return None

    def get_all_with_pagination(self, page: int, per_page: int):
        try:
            tasks = self.session.query(TaskEntity).offset((page - 1) * per_page).limit(per_page).all()
            log.info(f"Got tasks for page {page} with {per_page} tasks per page")
            return tasks
        except Exception as e:
            log.error(f"Error getting tasks: {e}")
            return None

    def filter(self, **kwargs):
        try:
            tasks = self.session.query(TaskEntity).filter_by(**kwargs).all()
            return tasks
        except Exception as e:
            log.error(f"Error filtering tasks: {e}")
            return None

    def update(self, task_id, data):
        try:
            task = self.session.query(TaskEntity).get(task_id)
            for key, value in data.items():
                setattr(task, key, value)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            log.error(f"Error updating task: {e}")
            return False

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
                self.session.execute(
                    update(TaskEntity),
                    chunk
                )
                self.session.commit()
                total_updated += len(chunk)
                log.info(f"Updated chunk {i // chunk_size + 1} successfully")
            except Exception as e:
                self.session.rollback()
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

    def delete(self, task_id):
        try:
            task = self.session.query(TaskEntity).get(task_id)
            self.session.delete(task)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            log.error(f"Error deleting task: {e}")
            return None

    def bulk_delete(self, task_ids):
        try:
            stmt = delete(TaskEntity).where(TaskEntity.id.in_(task_ids))
            self.session.execute(stmt)
            self.session.commit()
            log.info(f"Deleted tasks: {task_ids}")
            return True
        except Exception as e:
            self.session.rollback()
            log.error(f"Error deleting tasks: {e}")
            return False
