from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotFileRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotFileRepository
from app.runner.config import Config
from app.services.actions import ActionsService
from app.services.buildings import BuildingsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService
from app.services.websocket import WebSocketService
from app.services.world_entities import WorldEntities


@dataclass
class JsonFileRepository:
    snapshot_path: str

    def people(self) -> PeopleSnapshotFileRepository:
        return PeopleSnapshotFileRepository(
            snapshot_file=Path(self.snapshot_path) / "people.json"
        )

    def buildings(self) -> BuildingsSnapshotFileRepository:
        return BuildingsSnapshotFileRepository(
            snapshot_file=Path(self.snapshot_path) / "buildings.json"
        )


@dataclass
class ServiceFactory:
    config: Config

    @cached_property
    def websocket_manager(self) -> WebSocketService:
        return WebSocketService()

    @cached_property
    def buildings_service(self) -> BuildingsService:
        return BuildingsService(buildings=BuildingsInMemoryRepository())

    @cached_property
    def people_service(self) -> PeopleService:
        return PeopleService(people=PeopleInMemoryRepository())

    @cached_property
    def actions_service(self) -> ActionsService:
        return ActionsService(people=self.people_service)

    @cached_property
    def movement_service(self) -> MovementService:
        return MovementService(
            grid_size=self.config.GRID_SIZE,
            buildings=self.buildings_service,
            people=self.people_service,
        )

    @cached_property
    def snapshot_service(self) -> SnapshotService | None:
        if not self.config.SNAPSHOT_PATH:
            return None

        if not self.config.SNAPSHOT_INTERVAL:
            raise ValueError("SNAPSHOT_INTERVAL is required when SNAPSHOT_PATH is set")

        json_repository = JsonFileRepository(snapshot_path=self.config.SNAPSHOT_PATH)

        return SnapshotService(
            people_snapshot_repository=json_repository.people(),
            buildings_snapshot_repository=json_repository.buildings(),
            people_service=self.people_service,
            buildings_service=self.buildings_service,
            interval_seconds=int(self.config.SNAPSHOT_INTERVAL),
        )

    @cached_property
    def simulation_service(self) -> SimulationService:
        return SimulationService(
            websocket_manager=self.websocket_manager,
            people=self.people_service,
            movement=self.movement_service,
            actions=self.actions_service,
        )

    @cached_property
    def world_entities(self) -> WorldEntities:
        return WorldEntities(
            snapshot_service=self.snapshot_service,
            grid_size=self.config.GRID_SIZE,
            people_amount=self.config.PEOPLE_AMOUNT,
            building_amount=self.config.BUILDINGS_AMOUNT,
            buildings_service=self.buildings_service,
            people_service=self.people_service,
            killer_probability=self.config.KILLER_PROBABILITY,
            police_probability=self.config.POLICE_PROBABILITY,
        )
