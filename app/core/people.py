import random
from dataclasses import dataclass, field

from app.core.person import Person
from app.repositories.people import PeopleJsonRepository


@dataclass
class PeopleService:
    repository: PeopleJsonRepository
    people: list[Person] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        snapshot = self.repository.load_snapshot()

        if snapshot is None:
            self.people = self.create_many()
        else:
            self.people = snapshot

    @staticmethod
    def create_many(count: int = 100) -> list[Person]:
        return [
            Person(id=i, x=random.randint(0, 99), y=random.randint(0, 99))
            for i in range(count)
        ]

    def get_all(self) -> list[Person]:
        return self.people

    def update_positions(self) -> None:
        for person in self.people:
            person.x = (person.x + random.choice([-1, 0, 1])) % 100
            person.y = (person.y + random.choice([-1, 0, 1])) % 100

    def save_snapshot(self) -> None:
        self.repository.save_snapshot(self.people)
