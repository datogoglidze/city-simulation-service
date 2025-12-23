from functools import cache
from pathlib import Path

from app.config import config
from app.repositories.people import PeopleInMemoryRepository
from app.repositories.people_snapshot import SnapshotJsonRepository
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService


@cache
def get_snapshot_repository() -> SnapshotJsonRepository:
    return SnapshotJsonRepository(snapshot_file=Path(config.SNAPSHOT_PATH))


@cache
def get_people_repository() -> PeopleInMemoryRepository:
    return PeopleInMemoryRepository()


@cache
def get_people_service() -> PeopleService:
    return PeopleService(
        people=get_people_repository(),
        snapshot=get_snapshot_repository(),
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
    )


@cache
def get_websocket_manager() -> WebSocketManager:
    return WebSocketManager()


@cache
def get_simulation_service() -> SimulationService:
    return SimulationService(
        websocket_manager=get_websocket_manager(),
        people=get_people_service(),
        snapshot_interval=config.SNAPSHOT_INTERVAL,
        snapshot=get_snapshot_repository(),
    )
