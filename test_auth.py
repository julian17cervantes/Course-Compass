from fastapi.testclient import TestClient

from main import app

COURSE = {
    "name": "Intro to Programming",
    "code": "CS101",
    "units": 3,
    "grade": "A",
    "semester": "Fall 2025",
}


def test_courses_require_login(client):
    anonymous = TestClient(app)
    assert anonymous.get("/courses").status_code == 401
    assert anonymous.post("/courses", json=COURSE).status_code == 401
    assert anonymous.get("/gpa").status_code == 401


def test_signup_duplicate_email(client):
    user = {"email": "dupe@example.com", "password": "password123"}
    assert client.post("/signup", json=user).status_code == 201
    assert client.post("/signup", json=user).status_code == 400


def test_login_wrong_password(client):
    response = client.post("/login", data={"username": "test@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_users_cannot_see_each_others_courses(client):
    created = client.post("/courses", json=COURSE).json()

    other = TestClient(app)
    other.post("/signup", json={"email": "other@example.com", "password": "password123"})
    login = other.post("/login", data={"username": "other@example.com", "password": "password123"})
    other.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})

    assert other.get("/courses").json() == []
    assert other.get(f"/courses/{created['id']}").status_code == 404
    assert other.delete(f"/courses/{created['id']}").status_code == 404

def make_other_client():
    other = TestClient(app)
    other.post("/signup", json={"email": "other@example.com", "password": "password123"})
    login = other.post(
        "/login", data={"username": "other@example.com", "password": "password123"}
    )
    other.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return other


def test_owner_can_update_any_of_their_courses(client):
    client.post("/courses", json=COURSE)
    second = client.post("/courses", json={**COURSE, "code": "MATH101"}).json()
    response = client.put(f"/courses/{second['id']}", json={"grade": "B"})
    assert response.status_code == 200
    assert response.json()["grade"] == "B"


def test_other_user_cannot_update_a_course_with_a_matching_id(client):
    client.post("/courses", json=COURSE)
    second = client.post("/courses", json={**COURSE, "code": "MATH101"}).json()
    other = make_other_client()  # this account is user 2, and the course above is course 2
    response = other.put(f"/courses/{second['id']}", json={"grade": "F"})
    assert response.status_code == 404
    assert client.get(f"/courses/{second['id']}").json()["grade"] == "A"