from starlette.testclient import TestClient


def test_should_not_read_when_does_not_exist(client: TestClient) -> None:
    response = client.get("/locations/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Location with id 1 not found"}


def test_should_read_many(client: TestClient) -> None:
    response = client.get("/locations")

    assert response.status_code == 200
    assert len(response.json()) > 1
