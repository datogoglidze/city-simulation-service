from pathlib import Path

import pytest
from starlette.testclient import TestClient

from app.repositories.people import (
    PeopleInMemoryRepository,
    PeopleSnapshotJsonRepository,
)
from app.runner.config import config
from app.runner.fastapi import FastApiConfig
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@pytest.fixture
def client() -> TestClient:
    websocket_manager = WebSocketManager()
    snapshot_repository = PeopleSnapshotJsonRepository(
        snapshot_file=Path(config.SNAPSHOT_PATH)
    )
    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        snapshot=snapshot_repository,
        grid_size=10,
        people_amount=0,
    )

    return TestClient(
        app=FastApiConfig(
            websocket=websocket_manager,
            simulation=SimulationService(
                websocket_manager=websocket_manager,
                snapshot=snapshot_repository,
                people=people_service,
                snapshot_interval=100,
            ),
            people=people_service,
        ).setup()
    )
