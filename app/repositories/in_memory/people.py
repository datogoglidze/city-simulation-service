from dataclasses import dataclass, field
from typing import Any, Iterator

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Person
from app.repositories.in_memory.indexes import IndexManager


@dataclass
class PeopleInMemoryRepository:
    _people: dict[str, Person] = field(default_factory=dict)

    indexes: IndexManager[Person, str] = field(
        default_factory=lambda: IndexManager(
            extractors={
                "q": lambda person: person.location.q,
                "r": lambda person: person.location.r,
                "is_dead": lambda person: person.is_dead,
            }
        )
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
        self.indexes.create_one(person.id, person)

        return person

    def delete_one(self, person_id: str) -> None:
        person = self._people.get(person_id)
        if not person:
            raise DoesNotExistError(person_id)

        self.indexes.delete_one(person_id, person)
        self._people.pop(person_id, None)

    def update_one(self, person: Person) -> None:
        existing = self._people.get(person.id)
        if not existing:
            raise DoesNotExistError(person.id)

        self.indexes.update_one(person.id, existing, person)
        self._people[person.id] = person

    def read_many(self, **params: Any) -> Iterator[Person]:
        if not params:
            return iter(self._people.values())

        people_ids = self.indexes.read_many(**params)

        people = []
        for person_id in people_ids:
            person = self._people.get(person_id)
            if person is not None:
                people.append(person)

        return iter(people)
