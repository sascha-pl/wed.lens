from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.photo import Photo


def test_api_delete_photo(
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

    response = authenticated_client.delete(
        f"/api/photo/{photo_id}",
    )

    assert response.status_code == 204

    deleted_photo = db.get(Photo, photo_id)
    assert deleted_photo is not None
    assert deleted_photo.is_deleted is True