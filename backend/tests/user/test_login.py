
from argon2 import PasswordHasher
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.services.user_service import UserService

client = TestClient(app)


def test_api_login(db: Session) -> None:
    password_hasher = PasswordHasher()

    UserService(db).create_user(
        name="Jane Doe",
        email="jane@example.com",
        password_hash=password_hasher.hash("more-secret-password"),
    )

    db.commit()

    response = client.post(
        "/api/user/login",
        json={
            "email": "jane@example.com",
            "password": "more-secret-password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["authenticated"] is True

    assert "session" not in data
    assert "session_key" not in data
    assert "password" not in data
    assert "password_hash" not in data
    assert "session_key" in response.cookies

    session_key = response.cookies["session_key"]

    assert isinstance(session_key, str)
    assert len(session_key) == 64