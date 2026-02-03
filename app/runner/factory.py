from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository


@dataclass
class JsonRepository:
    people_snapshot_repository: PeopleSnapshotJsonRepository
    buildings_snapshot_repository: BuildingsSnapshotJsonRepository

    @staticmethod
    def from_path(snapshot_path: str) -> JsonRepository:
        return JsonRepository(
            people_snapshot_repository=PeopleSnapshotJsonRepository(
                snapshot_file=Path(snapshot_path) / "people.json"
            ),
            buildings_snapshot_repository=BuildingsSnapshotJsonRepository(
                snapshot_file=Path(snapshot_path) / "buildings.json"
            ),
        )
