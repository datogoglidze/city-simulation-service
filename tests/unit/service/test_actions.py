import pytest

from tests.fake import FakePerson

from app.models.person import Location, Person, PersonRole
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.actions import ActionsService
from app.services.people import PeopleService


@pytest.fixture
def person() -> Person:
    return FakePerson(location=Location(q=0, r=0), role=PersonRole.killer).entity


@pytest.fixture
def people_service(person: Person) -> PeopleService:
    people_repository = PeopleInMemoryRepository()
    people_repository.create_one(person)

    return PeopleService(people=people_repository)


@pytest.fixture
def actions_service(people_service: PeopleService) -> ActionsService:
    return ActionsService(people=people_service)


def test_killer_should_kill_citizen(
    actions_service: ActionsService, people_service: PeopleService, person: Person
) -> None:
    citizen = FakePerson(location=Location(q=0, r=1), role=PersonRole.citizen).entity
    people_service.create_one(citizen)

    actions_service.kill()

    assert people_service.read_all() == [person]


def test_killer_should_not_kill_killer(
    actions_service: ActionsService, people_service: PeopleService, person: Person
) -> None:
    killer = FakePerson(location=Location(q=0, r=1), role=PersonRole.killer).entity
    people_service.create_one(killer)

    actions_service.kill()

    assert people_service.read_all() == [person, killer]
