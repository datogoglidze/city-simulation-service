import json
from dataclasses import dataclass
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

    def load(self) -> SnapshotData:
        if not self.snapshot_file.exists():
            raise FileNotFoundError(f"Snapshot file not found at {self.snapshot_file}")

        raw = json.loads(self.snapshot_file.read_text())

        # Step 1: Create locations (without people)
        existing_locations = {
            location["id"]: Location(
                id=location["id"], q=location["q"], r=location["r"], people=[]
            )
            for location in raw.get("locations", [])
        }

        people = [
            Person(id=person["id"], location=existing_locations[person["location_id"]])
            for person in raw.get("people", [])
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

        return SnapshotData(people=people, locations=locations)
