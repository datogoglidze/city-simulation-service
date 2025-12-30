import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Location, Person


@dataclass
class PeopleInMemoryRepository:
    _people: dict[str, Person] = field(default_factory=dict)

    def __len__(self) -> int:  # pragma: no cover
        return len(self._people)

    def __iter__(self) -> Iterator[Person]:  # pragma: no cover
        return iter(self._people.values())

    def read_all(self) -> list[Person]:
        return list(self._people.values())

    def read_one(self, person_id: str) -> Person:
        person = self._people.get(person_id)
        if not person:
            raise DoesNotExistError(person_id)

        return person

    def create_one(self, person: Person) -> Person:
        existing = self._people.get(person.id)
        if existing:
            raise ExistsError(existing.id)

        self._people[person.id] = person

        return person

    def delete_one(self, person_id: str) -> None:
        person = self._people.get(person_id)
        if not person:
            raise DoesNotExistError(person_id)

        self._people.pop(person_id, None)

    def update_one(self, person: Person) -> None:
        existing = self._people.get(person.id)
        if not existing:
            raise DoesNotExistError(person.id)

        self._people[person.id] = person


@dataclass
class PeopleSnapshotJsonRepository:
    snapshot_file: Path

    def __post_init__(self) -> None:
        self.snapshot_file.parent.mkdir(exist_ok=True)

    def save(self, people: list[Person]) -> None:
        raw = [asdict(p) for p in people]
        self.snapshot_file.write_text(json.dumps(raw, indent=2))

    def load(self) -> list[Person] | None:
        if not self.snapshot_file.exists():
            return None

        raw = json.loads(self.snapshot_file.read_text())

        return [
            Person(id=person["id"], location=Location(**person["location"]))
            for person in raw
        ]
