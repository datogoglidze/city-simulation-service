from unittest.mock import ANY

from starlette.testclient import TestClient

from tests.fake import FakePerson


def test_should_read_nothing_when_nothing_exist(client: TestClient) -> None:
    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == []


def test_should_not_read_when_does_not_exist(client: TestClient) -> None:
    unknown_person_id = FakePerson().entity.id

    response = client.get(f"/people/{unknown_person_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Person with id {unknown_person_id} not found"
    }


def test_should_create_one(client: TestClient) -> None:
    person = FakePerson()

    response = client.post("/people", json=person.json())

    assert response.status_code == 201
    assert response.json() == {"id": ANY, **person.json()}


def test_should_read_one(client: TestClient) -> None:
    person = FakePerson()
    created = client.post("/people", json=person.json())

    response = client.get(f"/people/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {"id": created.json()["id"], **person.json()}


def test_should_read_many(client: TestClient) -> None:
    person_1 = FakePerson()
    person_2 = FakePerson()
    client.post("/people", json=person_1.json())
    client.post("/people", json=person_2.json())

    response = client.get("/people")

    assert response.status_code == 200
    assert response.json() == [
        {"id": ANY, **person_1.json()},
        {"id": ANY, **person_2.json()},
    ]


def test_should_not_delete_when_does_not_exist(client: TestClient) -> None:
    unknown_person_id = FakePerson().entity.id

    response = client.delete(f"/people/{unknown_person_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Person with id {unknown_person_id} not found"
    }


def test_should_delete_one(client: TestClient) -> None:
    person = FakePerson()
    created = client.post("/people", json=person.json())

    response = client.delete(f"/people/{created.json()['id']}")

    assert response.status_code == 204
