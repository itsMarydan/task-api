import csv
from datetime import datetime, timedelta


def generate_due_date(index):
    base_date = datetime(2023, 8, 6) + timedelta(days=index)
    return (base_date + timedelta(days=15)).strftime('%Y-%m-%dT00:00:00+00:00')


with open('../../tasks.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'description', 'completed', 'due_date', 'created_at', 'created_by']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(201, 401):  # Adjust the range to generate the desired number of entries
        title = f'Task {chr(i)}'
        description = f'This is the description for Task {chr(i)}'
        completed = 'True' if i % 2 == 0 else 'False'
        due_date = generate_due_date(i)
        created_at = (datetime(2023, 8, 6) + timedelta(hours=i)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        created_by = f'User{chr(i % 7 + 65)}'

        writer.writerow({'title': title, 'description': description, 'completed': completed,
                         'due_date': due_date, 'created_at': created_at, 'created_by': created_by})
