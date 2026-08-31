from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_user_create() -> None:
    response = client.post(
        "/api/user/create",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret-password",
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