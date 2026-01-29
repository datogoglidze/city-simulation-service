import pytest

from tests.fake import FakePerson

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.actions import ActionsService
from app.services.movement import MovementService
from app.services.people import PeopleService


@pytest.fixture
def person() -> Person:
    return FakePerson(location=Location(q=0, r=0)).entity


@pytest.fixture
def people_service(person: Person) -> PeopleService:
    people_repository = PeopleInMemoryRepository()
    people_repository.create_one(person)

    return PeopleService(people=people_repository)


@pytest.fixture
def actions_service(people_service: PeopleService) -> ActionsService:
    return ActionsService(people=people_service)


@pytest.fixture
def movement_service(
    people_service: PeopleService,
    actions_service: ActionsService,
) -> MovementService:
    return MovementService(grid_size=10, people=people_service)


def test_should_move_to_adjacent_location(
    person: Person,
    movement_service: MovementService,
) -> None:
    generated_location = movement_service._generate_random_adjacent_location_for(
        person=person
    )

    assert (
        abs(generated_location.q - person.location.q) == 1
        or abs(generated_location.r - person.location.r) == 1
    )


def test_should_stay_in_place_when_no_valid_moves(
    person: Person,
    people_service: PeopleService,
    movement_service: MovementService,
) -> None:
    people_service.create_one(FakePerson(location=Location(q=0, r=1)).entity)
    people_service.create_one(FakePerson(location=Location(q=1, r=0)).entity)

    generated_location = movement_service._generate_random_adjacent_location_for(
        person=person
    )

    assert generated_location == person.location
