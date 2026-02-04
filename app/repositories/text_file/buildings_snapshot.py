from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.models.building import Building
from app.models.location import Location


@dataclass
class BuildingsSnapshotFileRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(parents=True, exist_ok=True)

    def save(self, buildings: list[Building]) -> None:
        raw = {"buildings": [asdict(building) for building in buildings]}

        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> list[Building]:
        snapshot = self._fetch_snapshot()

        return [
            Building(
                id=building["id"],
                location=Location(**building["location"]),
            )
            for building in snapshot.buildings()
        ]

    def _fetch_snapshot(self) -> _RawSnapshotData:
        if not self.snapshot_file.exists():
            raise FileNotFoundError(f"Snapshot file not found at {self.snapshot_file}")

        return _RawSnapshotData(self.snapshot_file.read_text())


@dataclass
class _RawSnapshotData:
    raw: str

    @property
    def json(self) -> dict[str, Any]:
        return dict(json.loads(self.raw))

    def buildings(self) -> list[dict[str, Any]]:
        return list(self.json.get("buildings", []))
