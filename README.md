# Task Manager API

A REST API for managing tasks, built with FastAPI, SQLAlchemy and PostgreSQL.

This project started from a general FastAPI project layout and was built out with
its own models, endpoints, validation and test suite.

## Stack

- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- PostgreSQL (SQLite fallback for local dev/tests)
- pytest + httpx (TestClient)
- Docker / docker-compose

## Endpoints

| Method | Path          | Description        |
|--------|---------------|---------------------|
| GET    | /tasks        | List all tasks      |
| GET    | /tasks/{id}   | Get a single task   |
| POST   | /tasks        | Create a task        |
| PUT    | /tasks/{id}   | Update a task        |
| DELETE | /tasks/{id}   | Delete a task        |

## Run locally (SQLite, no Docker needed)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs available at http://127.0.0.1:8000/docs

## Run with Docker + PostgreSQL

```bash
docker compose up --build
```

## Run tests

```bash
pytest -v
```

## Environment variables

| Variable       | Default                     | Description            |
|----------------|------------------------------|-------------------------|
| DATABASE_URL   | sqlite:///./tasks.db         | SQLAlchemy connection string |

## Project structure

```
task-manager-api/
├── app/
│   ├── main.py        # FastAPI app and routes
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   ├── crud.py         # Database operations
│   └── database.py     # DB engine/session setup
├── tests/
│   └── test_tasks.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
