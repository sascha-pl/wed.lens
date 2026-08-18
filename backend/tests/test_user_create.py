from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_user_create() -> None:
    response = client.post(
        "/api/user_create",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret-password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] == True
    assert "password" not in data
    assert "password_hash" not in data