import asyncio
from unittest.mock import ANY

from starlette.testclient import TestClient

from app.models.person import PersonRoles
from app.services.movement import MovementService


def test_should_broadcast_person_via_websocket(client: TestClient) -> None:
    client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )
    client.post(
        "/people",
        json={"location": {"q": 1, "r": 1}, "role": PersonRoles.citizen.value},
    )

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        data = websocket.receive_json()

        assert data == [
            {
                "id": ANY,
                "location": {"q": 0, "r": 0},
                "role": PersonRoles.citizen.value,
            },
            {
                "id": ANY,
                "location": {"q": 1, "r": 1},
                "role": PersonRoles.citizen.value,
            },
        ]


def test_should_broadcast_updated_locations(
    client: TestClient, movement_service: MovementService
) -> None:
    client.post(
        "/people",
        json={"location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value},
    )

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        first_data = websocket.receive_json()
        assert first_data == [
            {"id": ANY, "location": {"q": 0, "r": 0}, "role": PersonRoles.citizen.value}
        ]

        movement_service.move_people_to_random_adjacent_location()

        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        second_data = websocket.receive_json()
        assert len(second_data) == 1
        assert second_data != first_data
