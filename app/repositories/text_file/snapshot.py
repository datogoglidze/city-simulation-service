import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.models.person import Location, Person


@dataclass
class SnapshotData:
    people: list[Person]
    locations: list[Location]


@dataclass
class SnapshotJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save(self, people: list[Person], locations: list[Location]) -> None:
        raw = {
            "people": [asdict(person) for person in people],
            "locations": [asdict(location) for location in locations],
        }

        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> SnapshotData:
        if not self.snapshot_file.exists():
            raise FileNotFoundError(f"Snapshot file not found at {self.snapshot_file}")

        raw = json.loads(self.snapshot_file.read_text())

        people = [
            Person(id=person["id"], location_id=person["location_id"])
            for person in raw.get("people", [])
        ]

        locations = [
            Location(
                id=loc["id"],
                q=loc["q"],
                r=loc["r"],
                people_ids=list(loc.get("people_ids", [])),
            )
            for loc in raw.get("locations", [])
        ]

        return SnapshotData(people=people, locations=locations)
