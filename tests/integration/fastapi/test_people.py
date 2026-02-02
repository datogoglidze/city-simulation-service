from unittest.mock import ANY

import pytest
from starlette.testclient import TestClient

from tests.fake import FakePerson

from app.models.person import PersonRole


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


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_create_one(client: TestClient, person_role: PersonRole) -> None:
    person = FakePerson(role=person_role)

    response = client.post("/people", json=person.json())

    assert response.status_code == 201
    assert response.json() == {"id": ANY, **person.json()}


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_read_one(client: TestClient, person_role: PersonRole) -> None:
    person = FakePerson(role=person_role)
    created = client.post("/people", json=person.json())

    response = client.get(f"/people/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {"id": created.json()["id"], **person.json()}


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_read_many_with_no_parameters(
    client: TestClient, person_role: PersonRole
) -> None:
    person_1 = FakePerson(role=person_role)
    person_2 = FakePerson(role=person_role)
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
