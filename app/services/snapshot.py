import asyncio
from dataclasses import dataclass

from app.models.building import Building
from app.models.person import Person
from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.buildings import BuildingsService
from app.services.people import PeopleService


@dataclass
class SnapshotService:
    people_snapshot_repository: PeopleSnapshotJsonRepository
    people_service: PeopleService

    buildings_snapshot_repository: BuildingsSnapshotJsonRepository
    buildings_service: BuildingsService

    interval_seconds: int

    def load_people(self) -> list[Person]:
        people = self.people_snapshot_repository.load()

        for person in people:
            self.people_service.create_one(person)

        return people

    def load_buildings(self) -> list[Building]:
        buildings = self.buildings_snapshot_repository.load()

        for building in buildings:
            self.buildings_service.create_one(building)

        return buildings

    def save_people(self) -> None:
        people = self.people_service.read_many()
        self.people_snapshot_repository.save(people)

    def save_buildings(self) -> None:
        buildings = self.buildings_service.read_many()
        self.buildings_snapshot_repository.save(buildings)

    async def run_periodic_save(self) -> None:
        while True:
            await asyncio.sleep(self.interval_seconds)
            self.save_people()
            self.save_buildings()
