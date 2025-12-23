from dataclasses import dataclass

from app.models.person import Person
from app.repositories.people import PeopleJsonRepository


@dataclass
class SnapshotService:
    repository: PeopleJsonRepository

    def save(self, people: list[Person]) -> None:
        self.repository.save_snapshot(people)

    def load(self) -> list[Person] | None:
        return self.repository.load_snapshot()
