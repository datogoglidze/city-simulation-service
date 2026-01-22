import pytest

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.movement import MovementService
from app.services.people import PeopleService


@pytest.fixture
def person() -> Person:
    return Person(id="1", location=Location(q=0, r=0))


@pytest.fixture
def people_service(person: Person) -> PeopleService:
    people_repository = PeopleInMemoryRepository()
    people_repository.create_one(person)

    return PeopleService(people=people_repository)


@pytest.fixture
def movement_service(people_service: PeopleService) -> MovementService:
    return MovementService(grid_size=10, people=people_service)


def test_should_move_to_adjacent_location(
    person: Person,
    movement_service: MovementService,
) -> None:
    moved_person = movement_service.move_to_random_adjacent_location(person=person)

    assert (
        abs(moved_person.location.q - person.location.q) == 1
        or abs(moved_person.location.r - person.location.r) == 1
    )


def test_should_stay_in_place_when_no_valid_moves(
    person: Person,
    people_service: PeopleService,
    movement_service: MovementService,
) -> None:
    people_service.create_one(Person(id="2", location=Location(q=0, r=1)))
    people_service.create_one(Person(id="3", location=Location(q=1, r=0)))

    moved_person = movement_service.move_to_random_adjacent_location(person=person)

    assert moved_person.location == person.location
