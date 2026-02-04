from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository


@dataclass
class JsonRepository:
    snapshot_path: str

    def people(self) -> PeopleSnapshotJsonRepository:
        return PeopleSnapshotJsonRepository(
            snapshot_file=Path(self.snapshot_path) / "people.json"
        )

    def buildings(self) -> BuildingsSnapshotJsonRepository:
        return BuildingsSnapshotJsonRepository(
            snapshot_file=Path(self.snapshot_path) / "buildings.json"
        )
