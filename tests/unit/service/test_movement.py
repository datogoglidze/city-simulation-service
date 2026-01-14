import pytest

from app.models.person import Location, Person
from app.services.movement import MovementService


@pytest.fixture
def movement_service() -> MovementService:
    return MovementService(grid_size=10)


def test_should_move_to_adjacent_location(movement_service: MovementService) -> None:
    person = Person(id="1", location=Location(q=5, r=5))

    moved_person = movement_service.move_to_random_adjacent_location(
        person=person, occupied_locations=set()
    )

    assert (
        abs(moved_person.location.q - person.location.q) == 1
        or abs(moved_person.location.r - person.location.r) == 1
    )


def test_should_not_move_out_of_grid(
    movement_service: MovementService,
) -> None:
    person = Person(id="1", location=Location(q=0, r=0))
    occupied = {
        Location(q=0, r=1),
        Location(q=1, r=0),
    }

    moved_person = movement_service.move_to_random_adjacent_location(
        person=person, occupied_locations=occupied
    )

    assert moved_person.location == person.location


def test_should_stay_in_place_when_no_valid_moves(
    movement_service: MovementService,
) -> None:
    person = Person(id="1", location=Location(q=5, r=5))
    occupied = {
        Location(q=6, r=5),
        Location(q=6, r=4),
        Location(q=5, r=4),
        Location(q=4, r=5),
        Location(q=4, r=6),
        Location(q=5, r=6),
    }

    moved_person = movement_service.move_to_random_adjacent_location(
        person=person, occupied_locations=occupied
    )

    assert moved_person.location == person.location
