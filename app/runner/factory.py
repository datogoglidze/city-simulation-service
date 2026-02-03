from pathlib import Path

from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.buildings import BuildingsService
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


class SnapshotFactory:
    @staticmethod
    def create(
        snapshot_path: str | None,
        snapshot_interval: str | None,
        buildings_service: BuildingsService,
        people_service: PeopleService,
    ) -> SnapshotService | None:
        if not snapshot_path:
            return None

        if not snapshot_interval:
            raise ValueError("SNAPSHOT_INTERVAL is required when SNAPSHOT_PATH is set")

        people_snapshot_repository = PeopleSnapshotJsonRepository(
            snapshot_file=Path(snapshot_path + "/people.json")
        )

        buildings_snapshot_repository = BuildingsSnapshotJsonRepository(
            snapshot_file=Path(snapshot_path + "/buildings.json")
        )

        return SnapshotService(
            buildings_snapshot_repository=buildings_snapshot_repository,
            buildings_service=buildings_service,
            people_snapshot_repository=people_snapshot_repository,
            people_service=people_service,
            interval_seconds=int(snapshot_interval),
        )
