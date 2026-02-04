import asyncio
from pathlib import Path

import pytest

from tests.fake import FakeBuilding, FakePerson

from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.buildings_snapshot import (
    BuildingsSnapshotJsonRepository,
)
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.services.buildings import BuildingsService
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


@pytest.fixture
def people_snapshot_repository() -> PeopleSnapshotJsonRepository:
    return PeopleSnapshotJsonRepository(
        snapshot_file=Path("data/test_people_snapshot.json")
    )


@pytest.fixture
def people_service() -> PeopleService:
    people_repository = PeopleInMemoryRepository()

    return PeopleService(people=people_repository)


@pytest.fixture
def buildings_snapshot_repository() -> BuildingsSnapshotJsonRepository:
    return BuildingsSnapshotJsonRepository(
        snapshot_file=Path("data/test_buildings_snapshot.json")
    )


@pytest.fixture
def buildings_service() -> BuildingsService:
    buildings_repository = BuildingsInMemoryRepository()

    return BuildingsService(buildings=buildings_repository)


@pytest.fixture
def snapshot_service(
    people_snapshot_repository: PeopleSnapshotJsonRepository,
    people_service: PeopleService,
    buildings_snapshot_repository: BuildingsSnapshotJsonRepository,
    buildings_service: BuildingsService,
) -> SnapshotService:
    return SnapshotService(
        people_snapshot_repository=people_snapshot_repository,
        people_service=people_service,
        buildings_snapshot_repository=buildings_snapshot_repository,
        buildings_service=buildings_service,
        interval_seconds=1,
    )


def test_should_raise_when_no_people_snapshot_exist(
    snapshot_service: SnapshotService,
) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot_service.load_people()


def test_should_raise_when_no_buildings_snapshot_exist(
    snapshot_service: SnapshotService,
) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot_service.load_buildings()


def test_should_load_people(
    people_snapshot_repository: PeopleSnapshotJsonRepository,
    people_service: PeopleService,
    snapshot_service: SnapshotService,
) -> None:
    person = FakePerson().entity
    people_snapshot_repository.save([person])

    loaded = snapshot_service.load_people()

    assert loaded == [person]

    people_snapshot_repository.snapshot_file.unlink()


def test_should_load_buildings(
    buildings_snapshot_repository: BuildingsSnapshotJsonRepository,
    buildings_service: BuildingsService,
    snapshot_service: SnapshotService,
) -> None:
    building = FakeBuilding().entity
    buildings_snapshot_repository.save([building])

    loaded = snapshot_service.load_buildings()

    assert loaded == [building]

    buildings_snapshot_repository.snapshot_file.unlink()


def test_should_save_people(
    people_snapshot_repository: PeopleSnapshotJsonRepository,
    people_service: PeopleService,
    snapshot_service: SnapshotService,
) -> None:
    person = FakePerson().entity
    people_service.create_one(person)
    snapshot_service.save_people()

    loaded = people_snapshot_repository.load()

    assert loaded == [person]

    people_snapshot_repository.snapshot_file.unlink()


def test_should_save_buildings(
    buildings_snapshot_repository: BuildingsSnapshotJsonRepository,
    buildings_service: BuildingsService,
    snapshot_service: SnapshotService,
) -> None:
    building = FakeBuilding().entity
    buildings_service.create_one(building)
    snapshot_service.save_buildings()

    loaded = buildings_snapshot_repository.load()

    assert loaded == [building]

    buildings_snapshot_repository.snapshot_file.unlink()


@pytest.mark.anyio
async def test_should_save_periodically(
    people_snapshot_repository: PeopleSnapshotJsonRepository,
    buildings_snapshot_repository: BuildingsSnapshotJsonRepository,
    people_service: PeopleService,
    buildings_service: BuildingsService,
    snapshot_service: SnapshotService,
) -> None:
    person = FakePerson().entity
    building = FakeBuilding().entity
    people_service.create_one(person)
    buildings_service.create_one(building)
    periodic_task = asyncio.create_task(snapshot_service.run_periodic_save())

    await asyncio.sleep(snapshot_service.interval_seconds + 1)
    periodic_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await periodic_task
    loaded_person = people_snapshot_repository.load()
    loaded_building = buildings_snapshot_repository.load()

    assert loaded_person == [person]
    assert loaded_building == [building]

    people_snapshot_repository.snapshot_file.unlink()
    buildings_snapshot_repository.snapshot_file.unlink()
