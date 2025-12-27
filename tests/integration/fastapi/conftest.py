from pathlib import Path

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.config import config
from app.repositories.people import PeopleInMemoryRepository
from app.repositories.people_snapshot import SnapshotJsonRepository
from app.runner.fastapi import FastApiConfig
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@pytest.fixture
def client() -> TestClient:
    websocket_manager = WebSocketManager()
    snapshot_repository = SnapshotJsonRepository(
        snapshot_file=Path(config.SNAPSHOT_PATH)
    )
    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        snapshot=snapshot_repository,
        grid_size=10,
        people_amount=0,
    )

    # Create app with lifespan disabled by default for most tests
    app = FastApiConfig(
        websocket=websocket_manager,
        simulation=SimulationService(
            websocket_manager=websocket_manager,
            snapshot=snapshot_repository,
            people=people_service,
            snapshot_interval=100,
        ),
        people=people_service,
    ).setup()
    
    # Disable lifespan for regular tests
    app.router.lifespan_context = None
    
    return TestClient(app=app, raise_server_exceptions=True)


@pytest.fixture
def client_with_simulation():
    """Client with simulation loop running in background."""
    websocket_manager = WebSocketManager()
    snapshot_repository = SnapshotJsonRepository(
        snapshot_file=Path(config.SNAPSHOT_PATH)
    )
    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        snapshot=snapshot_repository,
        grid_size=10,
        people_amount=0,
    )

    app = FastApiConfig(
        websocket=websocket_manager,
        simulation=SimulationService(
            websocket_manager=websocket_manager,
            snapshot=snapshot_repository,
            people=people_service,
            snapshot_interval=100,
        ),
        people=people_service,
    ).setup()
    
    # Return app, TestClient context manager will handle lifespan
    return TestClient(app=app, raise_server_exceptions=True)
