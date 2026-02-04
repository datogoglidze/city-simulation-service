from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotFileRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotFileRepository


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
