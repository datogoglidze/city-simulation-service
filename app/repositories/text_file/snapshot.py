from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.models.person import Location, Person
from app.models.snapshot import Snapshot


@dataclass
class SnapshotJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save(self, people: list[Person], locations: list[Location]) -> None:
        raw = {
            "people": [
                {"id": person.id, "location_id": person.location.id}
                for person in people
            ],
            "locations": [
                {"id": location.id, "q": location.q, "r": location.r}
                for location in locations
            ],
        }
        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> Snapshot:
        snapshot = self._fetch_snapshot()

        existing_locations = {
            location["id"]: Location(
                id=location["id"], q=location["q"], r=location["r"], people=[]
            )
            for location in snapshot.locations()
        }

        people = [
            Person(id=person["id"], location=existing_locations[person["location_id"]])
            for person in snapshot.people()
        ]

        people_by_location_id: dict[str, list[Person]] = {}
        for person in people:
            people_by_location_id.setdefault(person.location.id, []).append(person)

        locations = [
            Location(
                id=location.id,
                q=location.q,
                r=location.r,
                people=people_by_location_id.get(location.id, []),
            )
            for location in existing_locations.values()
        ]

        return Snapshot(people=people, locations=locations)

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

    def locations(self) -> list[dict[str, Any]]:
        return list(self.json.get("locations", []))

    def people(self) -> list[dict[str, Any]]:
        return list(self.json.get("people", []))
