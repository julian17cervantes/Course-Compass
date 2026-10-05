COURSE = {
    "name": "Intro to Programming",
    "code": "CECS 174",
    "units": 3,
    "grade": "A",
    "semester": "Fall 2025",
}


def test_create_course(client):
    response = client.post("/courses", json=COURSE)
    assert response.status_code == 201
    assert response.json()["code"] == "CS101"
    assert "id" in response.json()


def test_get_course_not_found(client):
    response = client.get("/courses/999")
    assert response.status_code == 404


def test_list_courses(client):
    client.post("/courses", json=COURSE)
    response = client.get("/courses")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_course(client):
    created = client.post("/courses", json=COURSE).json()
    response = client.put(f"/courses/{created['id']}", json={"grade": "B"})
    assert response.status_code == 200
    assert response.json()["grade"] == "B"
    assert response.json()["code"] == "CS101"


def test_delete_course(client):
    created = client.post("/courses", json=COURSE).json()
    assert client.delete(f"/courses/{created['id']}").status_code == 204
    assert client.get(f"/courses/{created['id']}").status_code == 404


def test_gpa_endpoint(client):
    client.post("/courses", json=COURSE)
    client.post("/courses", json={**COURSE, "code": "MATH101", "units": 1, "grade": "C"})
    response = client.get("/gpa")
    assert response.status_code == 200
    assert response.json()["cumulative_gpa"] == 3.5