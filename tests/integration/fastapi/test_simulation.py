from unittest.mock import ANY

from starlette.testclient import TestClient


def test_receive_initial_simulation_data(client_with_simulation: TestClient):
    """Test that client receives data from the simulation loop."""
    # Use context manager to enable lifespan
    with client_with_simulation as c:
        c.post("/people", json={"location": {"x": 0, "y": 0}})

        with c.websocket_connect("/simulation/ws") as websocket:
            # Wait for the simulation loop to broadcast (happens every 1 second)
            # Note: location will have changed due to update_location() in the loop
            response = websocket.receive_json()

            # Verify we receive data with correct structure
            assert len(response) == 1
            assert "location" in response[0]
            assert "id" in response[0]
            assert "x" in response[0]["location"]
            assert "y" in response[0]["location"]
