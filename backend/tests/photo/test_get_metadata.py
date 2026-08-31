from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_api_get_photo_metadata(
    db: Session,
    authenticated_client: TestClient,
) -> None:
    response = authenticated_client.post(
        "/api/photo/upload",
        files={
            "file": (
                "test.jpg",
                BytesIO(b"fake image content"),
                "image/jpeg",
            ),
        },
    )

    assert response.status_code == 201

    photo_id = response.json()["id"]

    response = authenticated_client.get(
        f"/api/photo/{photo_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == photo_id
    assert data["content_type"] == "image/jpeg"
    assert data["size_bytes"] == len(b"fake image content")

    assert "content" not in data