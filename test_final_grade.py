from fastapi.testclient import TestClient

from main import app


def test_final_grade_requires_login(client):
    anonymous = TestClient(app)
    response = anonymous.post(
        "/final-grade",
        json={"current_percent": 90, "final_weight_percent": 20, "target_percent": 85},)
    assert response.status_code == 401


def test_final_grade_achievable(client):
    response = client.post(
        "/final-grade",
        json={"current_percent": 90, "final_weight_percent": 20, "target_percent": 85},)
    assert response.status_code == 200
    assert response.json()["needed_on_final"] == 65.0
    assert response.json()["status"] == "achievable"


def test_final_grade_impossible(client):
    response = client.post(
        "/final-grade",
        json={"current_percent": 70, "final_weight_percent": 30, "target_percent": 90},)
    assert response.status_code == 200
    assert response.json()["status"] == "impossible"


def test_final_grade_rejects_bad_weight(client):
    response = client.post(
        "/final-grade",
        json={"current_percent": 90, "final_weight_percent": 0, "target_percent": 85},)
    assert response.status_code == 400