import asyncio
from unittest.mock import ANY

from starlette.testclient import TestClient

from tests.fake import FakePerson

from app.services.movement import MovementService


def test_should_broadcast_person_via_websocket(client: TestClient) -> None:
    person_1 = FakePerson()
    person_2 = FakePerson()
    client.post("/people", json=person_1.json())
    client.post("/people", json=person_2.json())

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        data = websocket.receive_json()

        assert data == [
            {"id": ANY, **person_1.json()},
            {"id": ANY, **person_2.json()},
        ]


def test_should_broadcast_updated_locations(
    client: TestClient, movement_service: MovementService
) -> None:
    person = FakePerson()
    client.post("/people", json=person.json())

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        first_data = websocket.receive_json()
        assert first_data == [{"id": ANY, **person.json()}]

        movement_service.move_people_to_random_adjacent_location()

        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        second_data = websocket.receive_json()
        assert len(second_data) == 1
        assert second_data != first_data
