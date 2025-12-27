import asyncio
from unittest.mock import ANY

from starlette.testclient import TestClient


def test_receive_initial_simulation_data(client: TestClient):
    client.post("/people", json={"location": {"x": 0, "y": 0}})

    with client.websocket_connect("/simulation/ws") as websocket:
        # Manually trigger broadcast from the test
        simulation = client.app.state.simulation
        asyncio.run(simulation.broadcast_state())
        
        response = websocket.receive_json()

        assert response == [{"location": {"x": 0, "y": 0}, "id": ANY}]
