import pytest

from argon2 import PasswordHasher
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app
from app.services.userservice import UserService

client = TestClient(app)


@pytest.fixture
def db() -> Session:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def test_api_login(db: Session) -> None:
    password_hasher = PasswordHasher()

    try:
        UserService(db).create_user(
            name="Jane Doe",
            email="jane@example.com",
            password_hash=password_hasher.hash("more-secret-password"),
        )

        db.commit()

        response = client.post(
            "/api/login",
            json={
                "email": "jane@example.com",
                "password": "more-secret-password",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True
        assert "password" not in data
        assert "password_hash" not in data

    finally:
        db.close()
