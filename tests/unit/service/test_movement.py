import pytest

from app.models.person import Location, Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.services.locations import LocationsService
from app.services.movement import MovementService


@pytest.fixture
def locations_service() -> LocationsService:
    service = LocationsService(locations=LocationsInMemoryRepository())
    # Create a 10x10 grid
    for q in range(10):
        for r in range(10):
            location = Location(id=f"{q}_{r}", q=q, r=r, people_ids=[])
            service.create_one(location)
    return service


@pytest.fixture
def movement_service(locations_service: LocationsService) -> MovementService:
    return MovementService(locations_service=locations_service)


def test_should_move_to_adjacent_location(
    movement_service: MovementService, locations_service: LocationsService
) -> None:
    person = Person(id="1", location_id="5_5")

    moved_person = movement_service.move_to_random_adjacent_location(person=person)

    # Get the actual locations
    original_loc = locations_service.read_one("5_5")
    moved_loc = locations_service.read_one(moved_person.location_id)

    # Should have moved to adjacent location
    assert (
        abs(moved_loc.q - original_loc.q) <= 1
        and abs(moved_loc.r - original_loc.r) <= 1
    )


def test_should_stay_in_place_when_no_valid_moves(
    movement_service: MovementService, locations_service: LocationsService
) -> None:
    person = Person(id="1", location_id="5_5")

    # Occupy all adjacent locations
    adjacent_ids = locations_service.get_adjacent_location_ids("5_5")
    for loc_id in adjacent_ids:
        loc = locations_service.read_one(loc_id)
        updated = Location(id=loc.id, q=loc.q, r=loc.r, people_ids=["other"])
        locations_service.update_one(updated)

    moved_person = movement_service.move_to_random_adjacent_location(person=person)

    assert moved_person.location_id == person.location_id
