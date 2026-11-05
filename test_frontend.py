import main


def test_root_returns_a_message_when_the_frontend_is_not_built(client, monkeypatch, tmp_path):
    monkeypatch.setattr(main, "FRONTEND_DIST", tmp_path)
    assert client.get("/").json() == {"message": "Course Compass is alive"}


def test_root_serves_the_built_page(client, monkeypatch, tmp_path):
    (tmp_path / "index.html").write_text("<html><body>Course Compass app</body></html>")
    monkeypatch.setattr(main, "FRONTEND_DIST", tmp_path)
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Course Compass app" in response.text