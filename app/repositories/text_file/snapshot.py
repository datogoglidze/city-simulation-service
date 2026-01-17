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
                {
                    "id": location.id,
                    "q": location.q,
                    "r": location.r,
                    "people_ids": [person.id for person in location.people],
                }
                for location in locations
            ],
        }

        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> SnapshotData:
        if not self.snapshot_file.exists():
            raise FileNotFoundError(f"Snapshot file not found at {self.snapshot_file}")

        raw = json.loads(self.snapshot_file.read_text())

        locations_dict = {}
        for loc_data in raw.get("locations", []):
            location = Location(
                id=loc_data["id"],
                q=loc_data["q"],
                r=loc_data["r"],
                people=[],
            )
            locations_dict[location.id] = location

        people = []
        for person_data in raw.get("people", []):
            location = locations_dict[person_data["location_id"]]
            person = Person(id=person_data["id"], location=location)
            people.append(person)

        people_by_location: dict[str, list[Person]] = {}
        for person in people:
            if person.location.id not in people_by_location:
                people_by_location[person.location.id] = []
            people_by_location[person.location.id].append(person)

        locations = []
        for location in locations_dict.values():
            location_people = people_by_location.get(location.id, [])
            updated_location = Location(
                id=location.id,
                q=location.q,
                r=location.r,
                people=location_people,
            )
            locations.append(updated_location)

        return SnapshotData(people=people, locations=locations)
