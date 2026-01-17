from dataclasses import dataclass

from app.models.person import Location, Person


@dataclass
class SnapshotData:
    people: list[Person]
    locations: list[Location]
