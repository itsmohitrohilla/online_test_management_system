import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def test_admin_create_question():
    response = client.post(
        "/admin/create_question",
        params={"admin_username": ADMIN_USERNAME, "question": "What is 2+2?", "answer": "4"},
        headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="}  # Base64 encoded "admin:password"
    )
    assert response.status_code == 200
    assert response.json()["question"] == "What is 2+2?"

def test_admin_read_questions():
    response = client.get("/admin/read_questions", headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_update_question():
    response = client.put(
        "/admin/update_question",
        params={"id": 1, "question": "What is 3+3?"},
        headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="}
    )
    assert response.status_code == 200
    assert response.json()["question"] == "What is 3+3?"

def test_admin_delete_question():
    response = client.delete("/admin/delete_question?id=1", headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    assert response.json() == {"message": "Question deleted successfully"}
