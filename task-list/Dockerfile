FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8000

CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT