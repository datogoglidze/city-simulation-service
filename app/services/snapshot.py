import asyncio
from dataclasses import dataclass

from app.models.building import Building
from app.models.person import Person
from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.building import BuildingService
from app.services.people import PeopleService


@dataclass
class SnapshotService:
    people_snapshot_repository: PeopleSnapshotJsonRepository
    people_service: PeopleService

    buildings_snapshot_repository: BuildingsSnapshotJsonRepository
    buildings_service: BuildingService

    interval_seconds: int

    def load_people(self) -> list[Person]:
        people = self.people_snapshot_repository.load()

        for person in people:
            self.people_service.create_one(person)

        return people

    async def run_people_periodic_save(self) -> None:
        while True:
            await asyncio.sleep(self.interval_seconds)
            people = self.people_service.read_many()

            self.people_snapshot_repository.save(people)

    def load_buildings(self) -> list[Building]:
        buildings = self.buildings_snapshot_repository.load()

        for building in buildings:
            self.buildings_service.create_one(building)

        return buildings

    async def run_buildings_periodic_save(self) -> None:
        while True:
            await asyncio.sleep(self.interval_seconds)
            buildings = self.buildings_service.read_many()

            self.buildings_snapshot_repository.save(buildings)
