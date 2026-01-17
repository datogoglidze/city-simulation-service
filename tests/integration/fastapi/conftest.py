import pytest
from starlette.testclient import TestClient

from app.models.person import Location
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import locations, people, simulation
from app.runner.fastapi import CityApi
from app.runner.websocket import WebSocketManager
from app.services.locations import LocationsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@pytest.fixture
def client() -> TestClient:
    websocket_manager = WebSocketManager()

    locations_repository = LocationsInMemoryRepository()
    people_repository = PeopleInMemoryRepository()

    locations_service = LocationsService(
        locations=locations_repository,
        people=people_repository,
    )
    people_service = PeopleService(
        people=people_repository,
        locations=locations_repository,
    )
    movement_service = MovementService(
        people_service=people_service,
        locations_service=locations_service,
    )

    # Create a 10x10 grid of locations for testing
    for q in range(10):
        for r in range(10):
            location = Location(q=q, r=r, people_ids=[])
            locations_service.create_one(location)

    return TestClient(
        app=CityApi()
        .with_router(simulation.router)
        .with_router(people.router)
        .with_router(locations.router)
        .with_websocket_manager(websocket_manager)
        .with_simulation_service(
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
                movement=movement_service,
                locations=locations_service,
            )
        )
        .with_people_service(people_service)
        .with_locations_service(locations_service)
        .with_movement_service(movement_service)
        .build()
    )
