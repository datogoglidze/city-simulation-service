import random
from contextlib import suppress
from dataclasses import dataclass

from app.models.errors import DoesNotExistError
from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    snapshot: PeopleSnapshotJsonRepository
    grid_size: int
    people_amount: int

    def __post_init__(self) -> None:
        snapshot = self.snapshot.load()

        if snapshot:
            for person in snapshot:
                self.people.create_one(person)
        else:
            self.create_random(count=self.people_amount)

    def _random_person(self) -> Person:
        return Person(
            location=Location(
                x=random.randint(0, self.grid_size - 1),
                y=random.randint(0, self.grid_size - 1),
            )
        )

    def create_random(self, count: int) -> list[Person]:
        return [self.people.create_one(self._random_person()) for _ in range(count)]

    def create_one(self, person: Person) -> Person:
        return self.people.create_one(person)

    def read_all(self) -> list[Person]:
        return list(self.people)

    def read_one(self, person_id: str) -> Person:
        return self.people.read_one(person_id)

    def delete_one(self, person_id: str) -> None:
        self.people.delete_one(person_id)

    def update_location(self) -> None:
        for person in self.people:
            new_location = self._random_neighboring_location(person)
            updated_person = Person(id=person.id, location=new_location)
            with suppress(DoesNotExistError):
                self.people.update_one(updated_person)

    def _random_neighboring_location(self, person: Person) -> Location:
        x = (person.location.x + random.choice([-1, 0, 1])) % self.grid_size
        y = (person.location.y + random.choice([-1, 0, 1])) % self.grid_size

        return Location(x=x, y=y)
