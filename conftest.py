import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import get_db
from main import app
from models import Base

TEST_USER = {"email": "test@example.com", "password": "password123"}

@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool,)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    test_client.post("/signup", json=TEST_USER)
    login = test_client.post("/login", data={"username": TEST_USER["email"], "password": TEST_USER["password"]},)
    token = login.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)