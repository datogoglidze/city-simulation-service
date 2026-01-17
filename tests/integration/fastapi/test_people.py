from unittest.mock import ANY

from starlette.testclient import TestClient


def test_should_read_nothing_when_nothing_exist(client: TestClient) -> None:
    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == []


def test_should_not_read_when_does_not_exist(client: TestClient) -> None:
    response = client.get("/people/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Person with id 1 not found"}


def test_should_not_create_when_location_unknown(client: TestClient) -> None:
    response = client.post("/people", json={"location_id": "1"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Location with id 1 not found"}


def test_should_create_one(client: TestClient) -> None:
    location = client.get("/locations").json()[0]
    response = client.post("/people", json={"location_id": location["id"]})

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY,
        "location": {
            "id": location["id"],
            "q": location["q"],
            "r": location["r"],
        },
    }


def test_should_read_one(client: TestClient) -> None:
    location = client.get("/locations").json()[0]
    created = client.post("/people", json={"location_id": location["id"]})
    response = client.get(f"/people/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "id": created.json()["id"],
        "location": {
            "id": location["id"],
            "q": location["q"],
            "r": location["r"],
        },
    }


def test_should_read_many(client: TestClient) -> None:
    location_1 = client.get("/locations").json()[0]
    location_2 = client.get("/locations").json()[1]
    client.post("/people", json={"location_id": location_1["id"]})
    client.post("/people", json={"location_id": location_2["id"]})

    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": ANY,
            "location": {
                "id": location_1["id"],
                "q": location_1["q"],
                "r": location_1["r"],
            },
        },
        {
            "id": ANY,
            "location": {
                "id": location_2["id"],
                "q": location_2["q"],
                "r": location_2["r"],
            },
        },
    ]


def test_should_not_delete_when_does_not_exist(client: TestClient) -> None:
    response = client.delete("/people/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Person with id 1 not found"}


def test_should_delete_one(client: TestClient) -> None:
    location = client.get("/locations").json()[0]
    created = client.post("/people", json={"location_id": location["id"]})
    response = client.delete(f"/people/{created.json()['id']}")

    assert response.status_code == 204
