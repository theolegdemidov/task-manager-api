import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Isolated in-memory SQLite database for tests (StaticPool keeps a single
# connection alive so the in-memory DB persists across requests).
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post(
        "/tasks", json={"title": "Buy milk", "description": "2 liters"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_requires_title():
    response = client.post("/tasks", json={"description": "no title"})
    assert response.status_code == 422


def test_get_task():
    created = client.post("/tasks", json={"title": "Read a book"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_missing_task_returns_404():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/tasks", json={"title": "Old title"}).json()
    response = client.put(
        f"/tasks/{created['id']}", json={"title": "New title", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True


def test_update_missing_task_returns_404():
    response = client.put("/tasks/999999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_task():
    created = client.post("/tasks", json={"title": "Temporary"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    follow_up = client.get(f"/tasks/{created['id']}")
    assert follow_up.status_code == 404


def test_delete_missing_task_returns_404():
    response = client.delete("/tasks/999999")
    assert response.status_code == 404
