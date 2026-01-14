import pytest

from app.models.person import Location
from app.services.movement import MovementService


@pytest.fixture
def movement_service() -> MovementService:
    return MovementService(grid_size=10)


def test_should_move_to_adjacent_location(movement_service: MovementService) -> None:
    location = Location(q=5, r=5)

    new_location = movement_service._calculate_next_location(location)

    assert (
        abs(new_location.q - location.q) == 1 or abs(new_location.r - location.r) == 1
    )


def test_should_stay_in_place_when_no_valid_moves(
    movement_service: MovementService,
) -> None:
    location = Location(q=5, r=5)
    occupied = {
        Location(q=6, r=5),
        Location(q=6, r=4),
        Location(q=5, r=4),
        Location(q=4, r=5),
        Location(q=4, r=6),
        Location(q=5, r=6),
    }
    movement_service.occupied_locations = occupied

    new_location = movement_service._calculate_next_location(location)

    assert new_location == location
