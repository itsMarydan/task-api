# API endpoints

## Single task - GET

``` text
/tasks/{task-id}
```

Returns:

``` json
{
    "id": 42,
    "title": "Get a coffee",
    "description": "Get a coffee, make sure it's a really good one!",
    "due_date": 2024-07-02,
    "completed": false,
    "created_at": 2023-07-01,
    "created_by": "Jane Doe"
}
```

## All tasks - GET

``` text
/tasks
```

Returns:

``` json
{
    "tasks": [
        {
            "id": 42,
            "title": "Get a coffee",
            "description": "Get a coffee, make sure it's a really good one!",
            "due_date": 2024-07-01,
            "completed": false,
            "created_at": 2023-07-01,
            "created_by": "Jane Doe"
        },
        {
            "id": 82,
            "title": "Get a new car",
            "description": "Make sure it's a 4x4",
            "due_date": 2025-12-01,
            "completed": false,
            "created_at": 2023-04-10,
            "created_by": "John Doe"
        }
    ]
}
```

### Create new task - POST

``` text
/tasks
```

POST body:

``` json
{
    "title": "Go the beach",
    "description": "Make sure it's at least 90 degrees",
    "due_date": "2025-06-01"
}
```

## Update task - PUT

``` text
/tasks/{task_id}
```

PUT body:

``` json
{
    "title": "Go the beach",
    "description": "Make sure it's at least 90 degrees",
    "due_date": "2025-06-01",
    "completed": true
}
```

## Delete task - DELETE

``` text
/tasks/{task_id}
```