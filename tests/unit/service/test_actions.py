import pytest

from tests.fake import FakePerson

from app.models.person import Location, PersonRole
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.actions import ActionsService
from app.services.people import PeopleService


@pytest.fixture
def people_service() -> PeopleService:
    return PeopleService(people=PeopleInMemoryRepository())


@pytest.fixture
def actions_service(people_service: PeopleService) -> ActionsService:
    return ActionsService(people=people_service)


def test_killer_should_not_kill_killer(
    actions_service: ActionsService, people_service: PeopleService
) -> None:
    killer_1 = FakePerson(location=Location(q=0, r=0), role=PersonRole.killer).entity
    people_service.create_one(killer_1)
    killer_2 = FakePerson(location=Location(q=0, r=1), role=PersonRole.killer).entity
    people_service.create_one(killer_2)
    actions_service.kill()

    victim = people_service.read_one(killer_2.id)

    assert not victim.is_dead


def test_killer_should_kill_citizen(
    actions_service: ActionsService, people_service: PeopleService
) -> None:
    killer = FakePerson(location=Location(q=0, r=0), role=PersonRole.killer).entity
    people_service.create_one(killer)
    citizen = FakePerson(location=Location(q=0, r=1), role=PersonRole.citizen).entity
    people_service.create_one(citizen)
    actions_service.kill()

    victim = people_service.read_one(citizen.id)

    assert victim.is_dead


def test_police_should_not_kill_citizen(
    actions_service: ActionsService, people_service: PeopleService
) -> None:
    police = FakePerson(location=Location(q=0, r=0), role=PersonRole.police).entity
    people_service.create_one(police)
    citizen = FakePerson(location=Location(q=0, r=1), role=PersonRole.citizen).entity
    people_service.create_one(citizen)
    actions_service.kill()

    victim = people_service.read_one(citizen.id)

    assert not victim.is_dead


def test_police_should_kill_killer(
    actions_service: ActionsService, people_service: PeopleService
) -> None:
    police = FakePerson(location=Location(q=0, r=0), role=PersonRole.police).entity
    people_service.create_one(police)
    killer = FakePerson(location=Location(q=0, r=1), role=PersonRole.killer).entity
    people_service.create_one(killer)
    actions_service.kill()

    victim = people_service.read_one(killer.id)

    assert victim.is_dead


def test_dead_person_should_not_kill(
    actions_service: ActionsService, people_service: PeopleService
) -> None:
    killer = FakePerson(
        location=Location(q=0, r=0), role=PersonRole.killer, is_dead=True
    ).entity
    people_service.create_one(killer)
    citizen = FakePerson(location=Location(q=0, r=1), role=PersonRole.citizen).entity
    people_service.create_one(citizen)
    actions_service.kill()

    victim = people_service.read_one(citizen.id)

    assert not victim.is_dead
