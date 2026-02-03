from unittest.mock import ANY

from starlette.testclient import TestClient

from tests.fake import FakeBuilding

from app.models.location import Location


def test_should_read_nothing_when_nothing_exist(client: TestClient) -> None:
    response = client.get("/buildings")

    assert response.status_code == 200
    assert response.json() == []


def test_should_not_read_when_does_not_exist(client: TestClient) -> None:
    unknown_building_id = FakeBuilding().entity.id

    response = client.get(f"/buildings/{unknown_building_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Building with id {unknown_building_id} not found"
    }


def test_should_create_one(client: TestClient) -> None:
    building = FakeBuilding()

    response = client.post("/buildings", json=building.json())

    assert response.status_code == 201
    assert response.json() == {"id": ANY, **building.json()}


def test_should_read_one(client: TestClient) -> None:
    building = FakeBuilding()
    created = client.post("/buildings", json=building.json())

    response = client.get(f"/buildings/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {"id": created.json()["id"], **building.json()}


def test_should_read_many_with_no_parameters(client: TestClient) -> None:
    building_1 = FakeBuilding()
    building_2 = FakeBuilding()
    client.post("/buildings", json=building_1.json())
    client.post("/buildings", json=building_2.json())

    response = client.get("/buildings")

    assert response.status_code == 200
    assert response.json() == [
        {"id": ANY, **building_1.json()},
        {"id": ANY, **building_2.json()},
    ]


def test_should_read_on_q_and_r(client: TestClient) -> None:
    building_1 = FakeBuilding(location=Location(q=0, r=0))
    building_2 = FakeBuilding()
    client.post("/buildings", json=building_1.json())
    client.post("/buildings", json=building_2.json())

    response = client.get("/buildings?q=0&r=0")

    assert response.status_code == 200
    assert response.json() == [{"id": ANY, **building_1.json()}]


def test_should_not_delete_when_does_not_exist(client: TestClient) -> None:
    unknown_building_id = FakeBuilding().entity.id

    response = client.delete(f"/buildings/{unknown_building_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Building with id {unknown_building_id} not found"
    }


def test_should_delete_one(client: TestClient) -> None:
    building = FakeBuilding()
    created = client.post("/buildings", json=building.json())

    response = client.delete(f"/buildings/{created.json()['id']}")

    assert response.status_code == 204
