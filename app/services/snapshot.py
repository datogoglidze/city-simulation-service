import asyncio
from dataclasses import dataclass

from app.models.person import Person
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.people import PeopleService


@dataclass
class SnapshotService:
    snapshot_repository: PeopleSnapshotJsonRepository
    people_service: PeopleService
    interval_seconds: int

    def load_people(self) -> list[Person]:
        people = self.snapshot_repository.load()

        for person in people:
            self.people_service.create_one(person)

        return people

    async def run_periodic_save(self) -> None:
        while True:
            await asyncio.sleep(self.interval_seconds)
            people = self.people_service.read_many()

            self.snapshot_repository.save(people)
