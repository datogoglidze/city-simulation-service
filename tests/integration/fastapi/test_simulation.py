import asyncio
from unittest.mock import ANY

from starlette.testclient import TestClient


def test_should_broadcast_person_via_websocket(client: TestClient) -> None:
    location_1 = client.get("/locations").json()[0]
    location_2 = client.get("/locations").json()[1]
    client.post("/people", json={"location_id": location_1["id"]})
    client.post("/people", json={"location_id": location_2["id"]})

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        data = websocket.receive_json()

        assert data == [
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


def test_should_broadcast_updated_locations(client: TestClient) -> None:
    location = client.get("/locations").json()[0]
    client.post("/people", json={"location_id": location["id"]})

    with client.websocket_connect("/simulation/ws") as websocket:
        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        first_data = websocket.receive_json()
        assert first_data == [
            {
                "id": ANY,
                "location": {
                    "id": location["id"],
                    "q": location["q"],
                    "r": location["r"],
                },
            }
        ]

        client.app.state.movement.move_all_people_randomly()  # type: ignore

        asyncio.run(client.app.state.simulation.broadcast_state())  # type: ignore

        second_data = websocket.receive_json()
        assert len(second_data) == 1
        assert second_data != first_data
