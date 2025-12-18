import random
from dataclasses import dataclass, field

from app.core.person import Person
from app.repositories.people import PeopleJsonRepository


@dataclass
class PeopleService:
    repository: PeopleJsonRepository
    grid_size: int
    people_amount: int

    people: list[Person] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.people = self.repository.load_snapshot() or self.create_many(
            count=self.people_amount
        )

    def create_many(self, count: int) -> list[Person]:
        return [
            Person(
                id=i,
                x=random.randint(0, self.grid_size - 1),
                y=random.randint(0, self.grid_size - 1),
            )
            for i in range(count)
        ]

    def get_all(self) -> list[Person]:
        return self.people

    def update_positions(self) -> None:
        for person in self.people:
            person.x = (person.x + random.choice([-1, 0, 1])) % self.grid_size
            person.y = (person.y + random.choice([-1, 0, 1])) % self.grid_size

    def save_snapshot(self) -> None:
        self.repository.save_snapshot(self.people)
