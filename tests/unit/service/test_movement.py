import pytest

from app.models.person import Location, Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.locations import LocationsService
from app.services.movement import MovementService
from app.services.people import PeopleService


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
    # Create a 10x10 grid
    for q in range(10):
        for r in range(10):
            location = Location(id=f"{q}_{r}", q=q, r=r, people=[])
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


def test_should_move_to_adjacent_location(
    movement_service: MovementService,
    people_service: PeopleService,
    locations_service: LocationsService,
) -> None:
    location = locations_service.read_one("5_5")
    person = Person(id="1", location=location)
    people_service.create_one(person)
    movement_service.add_person_to_location(person)

    # Pick a random adjacent location
    new_location = movement_service._pick_random_adjacent_location(person)
    assert new_location is not None

    # Get the actual locations
    original_loc = locations_service.read_one("5_5")
    moved_loc = locations_service.read_one(new_location.id)

    # Should be adjacent location
    assert (
        abs(moved_loc.q - original_loc.q) <= 1
        and abs(moved_loc.r - original_loc.r) <= 1
    )


def test_should_stay_in_place_when_no_valid_moves(
    movement_service: MovementService,
    people_service: PeopleService,
    locations_service: LocationsService,
) -> None:
    location = locations_service.read_one("5_5")
    person = Person(id="1", location=location)
    people_service.create_one(person)

    # Occupy all adjacent locations
    adjacent_locations = locations_service.get_adjacent_locations("5_5")
    for location in adjacent_locations:
        loc = locations_service.read_one(location.id)
        # Create a dummy person for each adjacent location
        dummy_person = Person(id="other", location=loc)
        updated = Location(id=loc.id, q=loc.q, r=loc.r, people=[dummy_person])
        locations_service.update_one(updated)

    new_location_id = movement_service._pick_random_adjacent_location(person)

    assert new_location_id is None
