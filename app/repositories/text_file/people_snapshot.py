from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.models.person import Location, Person, PersonRoles


@dataclass
class PeopleSnapshotJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save(self, people: list[Person]) -> None:
        raw = {"people": [asdict(person) for person in people]}

        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> list[Person]:
        snapshot = self._fetch_snapshot()

        return [
            Person(
                id=person["id"],
                location=Location(**person["location"]),
                role=PersonRoles(person["role"]),
            )
            for person in snapshot.people()
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

    def people(self) -> list[dict[str, Any]]:
        return list(self.json.get("people", []))
