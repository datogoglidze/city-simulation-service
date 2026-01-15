import pytest
from starlette.testclient import TestClient

from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.runner.fastapi import create_app
from app.runner.websocket import WebSocketManager
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@pytest.fixture
def client() -> TestClient:
    websocket_manager = WebSocketManager()

    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        movement=MovementService(grid_size=10),
    )

    return TestClient(
        app=create_app(
            websocket=websocket_manager,
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
            ),
            people_service=people_service,
        )
    )
