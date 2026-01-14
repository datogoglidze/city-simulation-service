import asyncio
from pathlib import Path

import pytest

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.hex_coordinate_strategies import OddRStrategy
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


@pytest.fixture
def snapshot_repository() -> PeopleSnapshotJsonRepository:
    return PeopleSnapshotJsonRepository(
        snapshot_file=Path("data/test_people_snapshot.json")
    )


@pytest.fixture
def people_service() -> PeopleService:
    return PeopleService(
        people=PeopleInMemoryRepository(),
        grid_size=10,
        coordinate_strategy=OddRStrategy(),
    )


@pytest.fixture
def snapshot_service(
    snapshot_repository: PeopleSnapshotJsonRepository, people_service: PeopleService
) -> SnapshotService:
    return SnapshotService(
        snapshot_repository=snapshot_repository,
        people_service=people_service,
        interval_seconds=1,
    )


def test_should_raise_when_nothing_exist(snapshot_service: SnapshotService) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot_service.load_people()


def test_should_load(
    snapshot_repository: PeopleSnapshotJsonRepository,
    people_service: PeopleService,
    snapshot_service: SnapshotService,
) -> None:
    person = Person(id="1", location=Location(q=0, r=0))
    snapshot_repository.save([person])

    loaded = snapshot_service.load_people()

    assert loaded == [person]

    snapshot_repository.snapshot_file.unlink()


@pytest.mark.anyio
async def test_should_save_periodically(
    snapshot_repository: PeopleSnapshotJsonRepository,
    people_service: PeopleService,
    snapshot_service: SnapshotService,
) -> None:
    person = Person(id="1", location=Location(q=0, r=0))
    people_service.create_one(person)
    periodic_task = asyncio.create_task(snapshot_service.run_periodic_save())

    await asyncio.sleep(snapshot_service.interval_seconds + 1)
    periodic_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await periodic_task
    loaded = snapshot_repository.load()

    assert loaded == [person]

    snapshot_repository.snapshot_file.unlink()
