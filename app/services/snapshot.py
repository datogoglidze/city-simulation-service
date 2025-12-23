from dataclasses import dataclass

from app.models.person import Person
from app.repositories.people_snapshot import PeopleJsonSnapshotRepository


@dataclass
class SnapshotService:
    repository: PeopleJsonSnapshotRepository

    def save(self, people: list[Person]) -> None:
        self.repository.save_snapshot(people)

    def load(self) -> list[Person] | None:
        return self.repository.load_snapshot()
