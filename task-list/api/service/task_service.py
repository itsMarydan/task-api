from api.repository.task_repo import TaskRepo


class TaskService:

    def __init__(self, session):
        self.repo = TaskRepo(session)

    def get_all(self):
        return self.repo.get_all()

    def get(self, task_id):
        return self.repo.get(task_id)

    def create(self, task):
        return self.repo.create(task)

    def update(self, task_id, task):
        return self.repo.update(task_id, task)

    def delete(self, task_id):
        return self.repo.delete(task_id)

    def bulk_create(self, tasks_data, chunk_size=100):
        return self.repo.bulk_create(tasks_data, chunk_size)

    def bulk_update(self, tasks_data, chunk_size=100):
        return self.repo.bulk_update(tasks_data, chunk_size)

    def bulk_delete(self, tasks_ids):
        return self.repo.bulk_delete(tasks_ids)

    def filter_by_status(self, completed):
        return self.repo.filter(completed=completed)

    def filter_by_status_and_due_date(self, completed, due_date):
        return self.repo.filter(status=completed, priority=due_date)
