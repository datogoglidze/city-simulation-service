from unittest.mock import ANY

from starlette.testclient import TestClient

from app.models.person import PersonRoles


def test_should_read_nothing_when_nothing_exist(client: TestClient) -> None:
    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == []


def test_should_not_read_when_does_not_exist(client: TestClient) -> None:
    response = client.get("/people/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Person with id 1 not found"}


def test_should_create_one(client: TestClient) -> None:
    response = client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY,
        "location": {"q": 0, "r": 0},
        "role": PersonRoles.citizen.value,
    }


def test_should_read_one(client: TestClient) -> None:
    created = client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )
    response = client.get(f"/people/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "id": created.json()["id"],
        "location": {"q": 0, "r": 0},
        "role": PersonRoles.citizen.value,
    }


def test_should_read_many(client: TestClient) -> None:
    client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )
    client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )

    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == [
        {"id": ANY, "location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
        {"id": ANY, "location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    ]


def test_should_not_delete_when_does_not_exist(client: TestClient) -> None:
    response = client.delete("/people/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Person with id 1 not found"}


def test_should_delete_one(client: TestClient) -> None:
    created = client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )
    response = client.delete(f"/people/{created.json()['id']}")

    assert response.status_code == 204
