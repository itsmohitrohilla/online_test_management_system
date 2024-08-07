import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user/create_user", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_take_test():
    response = client.get("/user/take_test", params={"username": "testuser"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_submit_answer():
    response = client.post("/user/submit_answer", params={"username": "testuser", "question_id": 1, "answer": "4"})
    assert response.status_code == 200
    assert response.json() == {"message": "Answer submitted successfully"}

def test_get_score():
    response = client.get("/user/get_score", params={"username": "testuser"})
    assert response.status_code == 200
    assert isinstance(response.json(), int)
