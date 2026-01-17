import asyncio
from unittest.mock import ANY

from starlette.testclient import TestClient


def test_should_broadcast_person_via_websocket(client: TestClient) -> None:
    client.post("/people", json={"location_id": "0_0"})
    client.post("/people", json={"location_id": "1_1"})

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        data = websocket.receive_json()

        assert data == [
            {"id": ANY, "location_id": "0_0"},
            {"id": ANY, "location_id": "1_1"},
        ]


def test_should_broadcast_updated_locations(client: TestClient) -> None:
    client.post("/people", json={"location_id": "5_5"})

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        first_data = websocket.receive_json()
        assert first_data == [{"id": ANY, "location_id": "5_5"}]

        client.app.state.movement.move_all_people_randomly()  # type: ignore

        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        second_data = websocket.receive_json()
        assert len(second_data) == 1
        # Location might have changed
        assert second_data[0]["id"] == first_data[0]["id"]
