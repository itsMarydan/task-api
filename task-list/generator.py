import json
import csv
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


# Generate random tasks
def generate_tasks(user_id, num_tasks):
    tasks = []
    for _ in range(num_tasks):
        task = {
            "title": fake.sentence(),
            "description": fake.paragraph(),
            "completed": fake.boolean(),
            "due_date": (datetime.utcnow() + timedelta(days=fake.random_int(1, 30))).isoformat() + "Z",
            "user_id": user_id
        }
        tasks.append(task)
    return tasks


user_1_tasks = generate_tasks(1, 200)
user_2_tasks = generate_tasks(2, 200)

# Export to JSON
with open('tasks_user_1.json', 'w') as json_file:
    json.dump(user_1_tasks, json_file, indent=4)

with open('tasks_user_2.json', 'w') as json_file:
    json.dump(user_2_tasks, json_file, indent=4)

# Export to CSV
csv_fields = ["title", "description", "completed", "due_date", "user_id"]

with open('tasks_user_1.csv', 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
    csv_writer.writeheader()
    csv_writer.writerows(user_1_tasks)

with open('tasks_user_2.csv', 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
    csv_writer.writeheader()
    csv_writer.writerows(user_2_tasks)
