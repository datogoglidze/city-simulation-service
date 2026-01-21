import asyncio
from dataclasses import dataclass

from app.models.snapshot import Snapshot
from app.repositories.text_file.snapshot import SnapshotJsonRepository
from app.services.locations import LocationsService
from app.services.people import PeopleService


@dataclass
class SnapshotService:
    snapshot_repository: SnapshotJsonRepository
    people_service: PeopleService
    locations_service: LocationsService
    interval_seconds: int

    def load_snapshot(self) -> Snapshot:
        snapshot_data = self.snapshot_repository.load()

        for location in snapshot_data.locations:
            self.locations_service.create_one(location)

        for person in snapshot_data.people:
            self.people_service.create_one(person)

        return snapshot_data

    async def run_periodic_save(self) -> None:
        while True:
            await asyncio.sleep(self.interval_seconds)
            people = self.people_service.read_all()
            locations = self.locations_service.read_all()

            self.snapshot_repository.save(people, locations)
