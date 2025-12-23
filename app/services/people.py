import random
from dataclasses import dataclass

from app.models.person import Location, Person
from app.repositories.people import PeopleInMemoryRepository
from app.repositories.people_snapshot import SnapshotJsonRepository


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    snapshot: SnapshotJsonRepository
    grid_size: int
    people_amount: int

    def __post_init__(self) -> None:
        loaded = self.snapshot.load()
        if loaded:
            for person in loaded:
                self.people.create_one(person)
        else:
            for person in self.create_many(count=self.people_amount):
                self.people.create_one(person)

    def create_many(self, count: int) -> list[Person]:
        return [
            Person(
                location=Location(
                    x=random.randint(0, self.grid_size - 1),
                    y=random.randint(0, self.grid_size - 1),
                ),
            )
            for _ in range(count)
        ]

    def read_all(self) -> list[Person]:
        return list(self.people)

    def update_location(self) -> None:
        for person in self.people:
            self._move_randomly_by_one(person)

    def _move_randomly_by_one(self, person: Person) -> None:
        person.location.x = (
            person.location.x + random.choice([-1, 0, 1])
        ) % self.grid_size
        person.location.y = (
            person.location.y + random.choice([-1, 0, 1])
        ) % self.grid_size
