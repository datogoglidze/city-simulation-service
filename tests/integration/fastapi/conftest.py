import pytest
from starlette.testclient import TestClient

from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import buildings, people, simulation
from app.runner.fastapi import CityApi
from app.services.actions import ActionsService
from app.services.buildings import BuildingsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.websocket import WebSocketService


@pytest.fixture
def buildings_service() -> BuildingsService:
    buildings_repository = BuildingsInMemoryRepository()
    return BuildingsService(buildings=buildings_repository)


@pytest.fixture
def people_service() -> PeopleService:
    people_repository = PeopleInMemoryRepository()
    return PeopleService(people=people_repository)


@pytest.fixture
def actions_service(people_service: PeopleService) -> ActionsService:
    return ActionsService(people=people_service)


@pytest.fixture
def movement_service(
    buildings_service: BuildingsService,
    people_service: PeopleService,
    actions_service: ActionsService,
) -> MovementService:
    return MovementService(
        grid_size=10, buildings=buildings_service, people=people_service
    )


@pytest.fixture
def client(
    buildings_service: BuildingsService,
    people_service: PeopleService,
    movement_service: MovementService,
    actions_service: ActionsService,
) -> TestClient:
    websocket_manager = WebSocketService()

    return TestClient(
        app=CityApi()
        .with_router(simulation.router)
        .with_router(buildings.router)
        .with_router(people.router)
        .with_websocket_manager(websocket_manager)
        .with_simulation_service(
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
                movement=movement_service,
                actions=actions_service,
            )
        )
        .with_buildings_service(buildings_service)
        .with_people_service(people_service)
        .build()
    )
