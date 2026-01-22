import pytest
from starlette.testclient import TestClient

from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import people, simulation
from app.runner.fastapi import CityApi
from app.runner.websocket import WebSocketManager
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@pytest.fixture
def people_repository() -> PeopleInMemoryRepository:
    return PeopleInMemoryRepository()


@pytest.fixture
def movement_service(people_repository: PeopleInMemoryRepository) -> MovementService:
    return MovementService(grid_size=10, people=people_repository)


@pytest.fixture
def client(
    people_repository: PeopleInMemoryRepository, movement_service: MovementService
) -> TestClient:
    websocket_manager = WebSocketManager()

    people_service = PeopleService(people=people_repository)

    return TestClient(
        app=CityApi()
        .with_router(simulation.router)
        .with_router(people.router)
        .with_websocket_manager(websocket_manager)
        .with_simulation_service(
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
                movement=movement_service,
            )
        )
        .with_people_service(people_service)
        .build()
    )
