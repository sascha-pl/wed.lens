from collections.abc import Generator

import pytest
from argon2 import PasswordHasher
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app
from app.models.user import User
from app.services.user_service import UserService


@pytest.fixture
def db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
        db.execute(
            delete(User)
        )
        db.commit()
        db.close()
    finally:
        db.close()
        
@pytest.fixture
def authenticated_client(db: Session) -> TestClient:
    password_hasher = PasswordHasher()

    UserService(db).create_user(
        name="Jane Doe",
        email="jane@example.com",
        password_hash=password_hasher.hash("more-secret-password"),
    )

    db.commit()

    client = TestClient(app)

    response = client.post(
        "/api/user/login",
        json={
            "email": "jane@example.com",
            "password": "more-secret-password",
        },
    )

    assert response.status_code == 200
    assert "session_key" in response.cookies

    print("CLIENT COOKIES:", client.cookies)

    return client