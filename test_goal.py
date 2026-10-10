from fastapi.testclient import TestClient

from main import app


def test_goal_requires_login(client):
    anonymous = TestClient(app)
    assert anonymous.get("/goal").status_code == 401
    assert anonymous.put("/goal", json={"goal_gpa": 3.5}).status_code == 401


def test_goal_must_be_set_first(client):
    assert client.get("/goal").status_code == 400


def test_goal_must_be_between_0_and_4(client):
    assert client.put("/goal", json={"goal_gpa": 4.5}).status_code == 400
    assert client.put("/goal", json={"goal_gpa": -1}).status_code == 400


def test_goal_plan(client):
    graded = {"name": "Intro", "code": "CS101", "units": 3, "grade": "A", "semester": "Fall 2025"}
    upcoming = {"name": "Data Structures", "code": "CS201", "units": 3, "semester": "Spring 2026"}
    client.post("/courses", json=graded)
    client.post("/courses", json=upcoming)

    assert client.put("/goal", json={"goal_gpa": 3.5}).status_code == 200
    plan = client.get("/goal").json()

    assert plan["status"] == "achievable"
    assert plan["required_average"] == 3.0
    assert plan["minimum_letter"] == "B"