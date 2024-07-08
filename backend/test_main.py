import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Idea
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_submit_idea(client, test_db):
    response = client.post("/submit_idea/", json={"description": "Test idea", "creator": "0xYourAddress", "private_key": "YourPrivateKey"})
    assert response.status_code == 200
    assert response.json()["description"] == "Test idea"


def test_get_idea(client, test_db):
    response = client.get("/get_idea/1")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test idea"
    assert data["creator"] == "0xYourAddress"