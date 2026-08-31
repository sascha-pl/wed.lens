from io import BytesIO

from fastapi.testclient import TestClient


def test_api_list_photos(
    authenticated_client: TestClient,
) -> None:
    for filename in ("one.jpg", "two.jpg"):
        response = authenticated_client.post(
            "/api/photo/upload",
            files={
                "file": (
                    filename,
                    BytesIO(b"fake image content"),
                    "image/jpeg",
                ),
            },
        )

        assert response.status_code == 201

    response = authenticated_client.get("/api/photo")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all("id" in photo for photo in data)
    assert all("content_type" in photo for photo in data)
    assert all("size_bytes" in photo for photo in data)