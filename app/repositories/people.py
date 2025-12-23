from dataclasses import dataclass, field
from typing import Iterator

from app.models.person import Person


@dataclass
class PeopleInMemoryRepository:
    _people: dict[int, Person] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self._people)

    def __iter__(self) -> Iterator[Person]:
        return iter(self._people.values())

    def get_all(self) -> list[Person]:
        return list(self._people.values())

    def get(self, person_id: int) -> Person | None:
        return self._people.get(person_id)

    def add(self, person: Person) -> None:
        self._people[person.id] = person

    def delete(self, person_id: int) -> None:
        self._people.pop(person_id, None)

    def update_position(self, person_id: int, x: int, y: int) -> None:
        person = self._people.get(person_id)
        if person:
            person.x = x
            person.y = y
