# DB Schema

TASK table:

``` database
- id (primary key)
- title (string)
- description (string)
- due_date (date)
- completed (boolean)
- created_at (timestamp)
- created_by (id of user who created task)
```

USER table:

``` text
- id (primary key)
- first_name (string)
- last_name (string)
```