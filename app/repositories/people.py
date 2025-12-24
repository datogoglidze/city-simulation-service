from dataclasses import dataclass, field
from typing import Iterator

from app.models.person import Person


@dataclass
class PeopleInMemoryRepository:
    _people: dict[str, Person] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self._people)

    def __iter__(self) -> Iterator[Person]:
        return iter(self._people.values())

    def read_all(self) -> list[Person]:
        return list(self._people.values())

    def read_one(self, person_id: str) -> Person | None:
        return self._people.get(person_id)

    def create_one(self, person: Person) -> Person:
        self._people[person.id] = person

        return person

    def delete_one(self, person_id: str) -> None:
        self._people.pop(person_id, None)

    def update_one(self, person: Person) -> None:
        if person.id in self._people:
            self._people[person.id] = person
