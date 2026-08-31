from uuid import uuid4

from fastapi.testclient import TestClient


def test_api_get_unknown_photo(
    authenticated_client: TestClient,
) -> None:
    response = authenticated_client.get(
        f"/api/photo/{uuid4()}",
    )

    assert response.status_code == 404