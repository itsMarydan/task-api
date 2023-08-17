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

## Notes
If you have issues when running tests, make sure you have the following installed:
* psycopg2-binary (pip install psycopg2-binary)

## Also see:
* [API documentation](api.md)
* [DB schema](db.md)