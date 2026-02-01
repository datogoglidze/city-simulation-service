from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Location, Person


@dataclass
class PeopleInMemoryRepository:
    _people: dict[str, Person] = field(default_factory=dict)

    _spatial_index: defaultdict[Location, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )

    def __len__(self) -> int:  # pragma: no cover
        return len(self._people)

    def __iter__(self) -> Iterator[Person]:  # pragma: no cover
        return iter(self._people.values())

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

        self.add_to_spatial_index(person)

        return person

    def delete_one(self, person_id: str) -> None:
        person = self._people.get(person_id)
        if not person:
            raise DoesNotExistError(person_id)

        self.remove_from_spatial_index(person)

        self._people.pop(person_id, None)

    def update_one(self, person: Person) -> None:
        existing = self._people.get(person.id)
        if not existing:
            raise DoesNotExistError(person.id)

        self.remove_from_spatial_index(existing)
        self.add_to_spatial_index(person)

        self._people[person.id] = person

    def read_at_locations(self, locations: set[Location]) -> list[Person]:
        people = []

        for location in locations:
            for person_id in self._spatial_index[location]:
                person = self._people.get(person_id)
                if person is not None:
                    people.append(person)

        return people

    def add_to_spatial_index(self, person: Person) -> None:
        self._spatial_index[person.location].add(person.id)

    def remove_from_spatial_index(self, person: Person) -> None:
        self._spatial_index[person.location].remove(person.id)
        if not self._spatial_index[person.location]:
            del self._spatial_index[person.location]
