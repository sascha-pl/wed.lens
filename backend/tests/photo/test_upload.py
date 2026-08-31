from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.photo import Photo
from app.models.storage_object import StorageObject


def test_api_upload_photo(
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

    data = response.json()

    assert "id" in data

    photo_id = data["id"]

    photo = db.get(Photo, photo_id)
    assert photo is not None

    storage_object = db.get(StorageObject, photo_id)
    assert storage_object is not None

    assert photo.content_type == "image/jpeg"
    assert photo.size_bytes == len(b"fake image content")