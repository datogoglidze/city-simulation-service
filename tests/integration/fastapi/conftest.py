from pathlib import Path

import pytest
from starlette.testclient import TestClient

from app.models.hex_coordinate import OddRStrategy
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.runner.fastapi import create_app
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService


@pytest.fixture
def client() -> TestClient:
    websocket_manager = WebSocketManager()

    snapshot_repository = PeopleSnapshotJsonRepository(
        snapshot_file=Path("test_people_snapshot.json")
    )

    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        grid_size=10,
        coordinate_strategy=OddRStrategy(),
    )

    return TestClient(
        app=create_app(
            websocket=websocket_manager,
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
            ),
            snapshot_service=(
                SnapshotService(
                    snapshot_repository=snapshot_repository,
                    people_service=people_service,
                    interval_seconds=100,
                )
            ),
            people_service=people_service,
        )
    )
