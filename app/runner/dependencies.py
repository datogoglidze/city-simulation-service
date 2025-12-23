from functools import cache
from pathlib import Path

from app.config import config
from app.repositories.people import PeopleJsonRepository
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService


@cache
def get_people_repository() -> PeopleJsonRepository:
    return PeopleJsonRepository(snapshot_file=Path(config.SNAPSHOT_PATH))


@cache
def get_snapshots() -> SnapshotService:
    return SnapshotService(repository=get_people_repository())


@cache
def get_people_service() -> PeopleService:
    return PeopleService(
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
        snapshot=get_snapshots(),
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
        snapshot=get_snapshots(),
    )
