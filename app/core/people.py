import random
from dataclasses import dataclass, field

from app.core.person import Person


@dataclass
class PeopleService:
    people: list[Person] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self._initialize_people()

    def _initialize_people(self, count: int = 10) -> None:
        self.people = [
            Person(id=i, x=random.randint(0, 99), y=random.randint(0, 99))
            for i in range(count)
        ]

    def get_all(self) -> list[Person]:
        return self.people

    def update_positions(self) -> None:
        for person in self.people:
            person.x = (person.x + random.choice([-1, 0, 1])) % 100
            person.y = (person.y + random.choice([-1, 0, 1])) % 100
