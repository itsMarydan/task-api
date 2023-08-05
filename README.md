# Task api
A sample app to demonstrate a simple API in written in Python leveraging a database and an Object-Relational Mapping (ORM) framework.

Technologies used in this project include:

* Python
* FastAPI
* Postgres
* SQLAlchemy
* Docker

## Run application
```bash
cd task-list
docker-compose up --build
```

## Start uvicorn server
```bash
cd task-list
uvicorn api.main:app --reload
```

## Also see:
* [API documentation](api.md)
* [DB schema](db.md)