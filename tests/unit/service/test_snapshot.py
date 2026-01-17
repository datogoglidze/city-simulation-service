import asyncio
from pathlib import Path

import pytest

from app.models.person import Location, Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.snapshot import SnapshotJsonRepository
from app.services.locations import LocationsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


@pytest.fixture
def snapshot_repository() -> SnapshotJsonRepository:
    return SnapshotJsonRepository(snapshot_file=Path("data/test_snapshot.json"))


@pytest.fixture
def locations_repository() -> LocationsInMemoryRepository:
    return LocationsInMemoryRepository()


@pytest.fixture
def people_repository() -> PeopleInMemoryRepository:
    return PeopleInMemoryRepository()


@pytest.fixture
def locations_service(
    locations_repository: LocationsInMemoryRepository,
    people_repository: PeopleInMemoryRepository,
) -> LocationsService:
    service = LocationsService(
        locations=locations_repository,
        people=people_repository,
    )
    # Create a location for testing
    location = Location(id="loc1", q=0, r=0, people=[])
    service.create_one(location)
    return service


@pytest.fixture
def people_service(
    people_repository: PeopleInMemoryRepository,
    locations_repository: LocationsInMemoryRepository,
) -> PeopleService:
    return PeopleService(
        people=people_repository,
        locations=locations_repository,
    )


@pytest.fixture
def movement_service(
    people_service: PeopleService, locations_service: LocationsService
) -> MovementService:
    return MovementService(
        people_service=people_service,
        locations_service=locations_service,
    )


@pytest.fixture
def snapshot_service(
    snapshot_repository: SnapshotJsonRepository,
    people_service: PeopleService,
    locations_service: LocationsService,
) -> SnapshotService:
    return SnapshotService(
        snapshot_repository=snapshot_repository,
        people_service=people_service,
        locations_service=locations_service,
        interval_seconds=1,
    )


def test_should_raise_when_nothing_exist(snapshot_service: SnapshotService) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot_service.load_snapshot()


def test_should_load(snapshot_repository: SnapshotJsonRepository) -> None:
    # Create fresh services for this test to avoid conflicts
    fresh_locations_repository = LocationsInMemoryRepository()
    fresh_people_repository = PeopleInMemoryRepository()
    fresh_locations_service = LocationsService(
        locations=fresh_locations_repository,
        people=fresh_people_repository,
    )
    fresh_people_service = PeopleService(
        people=fresh_people_repository,
        locations=fresh_locations_repository,
    )
    fresh_snapshot_service = SnapshotService(
        snapshot_repository=snapshot_repository,
        people_service=fresh_people_service,
        locations_service=fresh_locations_service,
        interval_seconds=1,
    )

    location = Location(id="loc1", q=0, r=0, people=[])
    person = Person(id="1", location=location)
    location_with_person = Location(id="loc1", q=0, r=0, people=[person])
    snapshot_repository.save([person], [location_with_person])

    loaded = fresh_snapshot_service.load_snapshot()

    assert len(loaded.people) == 1
    assert loaded.people[0].id == "1"
    assert loaded.people[0].location.id == "loc1"
    assert len(loaded.locations) == 1
    assert loaded.locations[0].id == "loc1"
    assert len(loaded.locations[0].people) == 1

    snapshot_repository.snapshot_file.unlink()


@pytest.mark.anyio
async def test_should_save_periodically(
    snapshot_repository: SnapshotJsonRepository,
    people_service: PeopleService,
    locations_service: LocationsService,
    movement_service: MovementService,
    snapshot_service: SnapshotService,
) -> None:
    location = locations_service.read_one("loc1")
    person = Person(id="1", location=location)
    people_service.create_one(person)
    # Add person to location tracking
    movement_service.add_person_to_location(person)

    periodic_task = asyncio.create_task(snapshot_service.run_periodic_save())

    await asyncio.sleep(snapshot_service.interval_seconds + 1)
    periodic_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await periodic_task
    loaded = snapshot_repository.load()

    assert len(loaded.people) == 1
    assert loaded.people[0].id == "1"
    # Location should have person in it
    assert any(loc.id == "loc1" and len(loc.people) == 1 for loc in loaded.locations)

    snapshot_repository.snapshot_file.unlink()
