from io import BytesIO

from fastapi.testclient import TestClient


def test_api_get_photo_content(
    authenticated_client: TestClient,
) -> None:
    content = b"fake image content"

    response = authenticated_client.post(
        "/api/photo/upload",
        files={
            "file": (
                "test.jpg",
                BytesIO(content),
                "image/jpeg",
            ),
        },
    )

    assert response.status_code == 201

    photo_id = response.json()["id"]

    response = authenticated_client.get(
        f"/api/photo/{photo_id}/content",
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content == content