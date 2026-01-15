from pathlib import Path

from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


class SnapshotFactory:
    @staticmethod
    def create(
        snapshot_path: str | None,
        snapshot_interval: str | None,
        people_service: PeopleService,
    ) -> SnapshotService | None:
        if not snapshot_path:
            return None

        if not snapshot_interval:
            raise ValueError("SNAPSHOT_INTERVAL is required when SNAPSHOT_PATH is set")

        snapshot_repository = PeopleSnapshotJsonRepository(
            snapshot_file=Path(snapshot_path)
        )

        return SnapshotService(
            snapshot_repository=snapshot_repository,
            people_service=people_service,
            interval_seconds=int(snapshot_interval),
        )
