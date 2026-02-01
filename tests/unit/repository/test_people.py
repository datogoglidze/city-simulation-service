import pytest

from tests.fake import FakePerson

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Person, PersonRole
from app.repositories.in_memory.people import PeopleInMemoryRepository


@pytest.fixture
def people() -> PeopleInMemoryRepository:
    return PeopleInMemoryRepository()


def test_should_read_nothing_when_nothing_exist(
    people: PeopleInMemoryRepository,
) -> None:
    existing_people = people

    assert len(existing_people) == 0


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_create_one(
    people: PeopleInMemoryRepository, person_role: PersonRole
) -> None:
    person = FakePerson(role=person_role).entity

    people.create_one(person)

    assert len(people) == 1


def test_should_not_duplicate_on_create_one(people: PeopleInMemoryRepository) -> None:
    person = FakePerson().entity
    people.create_one(person)

    with pytest.raises(ExistsError):
        people.create_one(person)


def test_should_not_read_when_does_not_exist(people: PeopleInMemoryRepository) -> None:
    with pytest.raises(DoesNotExistError):
        people.read_one(FakePerson().entity.id)


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_read_one(
    people: PeopleInMemoryRepository, person_role: PersonRole
) -> None:
    person = FakePerson(role=person_role).entity
    people.create_one(person)

    existing_person = people.read_one(person.id)

    assert existing_person == person


def test_should_not_delete_when_does_not_exist(
    people: PeopleInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        people.delete_one(FakePerson().entity.id)


def test_should_delete_one(people: PeopleInMemoryRepository) -> None:
    person = FakePerson().entity
    people.create_one(person)

    people.delete_one(person.id)

    assert len(people) == 0


def test_should_not_update_when_does_not_exist(
    people: PeopleInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        people.update_one(FakePerson().entity)


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_update_one(
    people: PeopleInMemoryRepository, person_role: PersonRole
) -> None:
    new = FakePerson(role=person_role).entity
    created = people.create_one(new)
    updated = FakePerson(role=person_role).entity
    person = Person(
        id=new.id,
        location=updated.location,
        role=updated.role,
        is_dead=updated.is_dead,
        lifespan=updated.lifespan,
    )
    people.update_one(person)

    updated_person = people.read_one(created.id)

    assert updated_person == person


def test_spatial_index_updated_on_create(people: PeopleInMemoryRepository) -> None:
    person = FakePerson().entity

    people.create_one(person)

    assert people.read_at_locations({person.location}) == [person]


def test_spatial_index_updated_on_delete(people: PeopleInMemoryRepository) -> None:
    person = FakePerson().entity
    people.create_one(person)
    people.delete_one(person.id)

    assert people.read_at_locations({person.location}) == []


def test_spatial_index_updated_on_update(people: PeopleInMemoryRepository) -> None:
    new = FakePerson().entity
    people.create_one(new)

    updated = FakePerson().entity
    person = Person(
        id=new.id,
        location=updated.location,
        role=updated.role,
        is_dead=updated.is_dead,
        lifespan=updated.lifespan,
    )

    people.update_one(person)

    assert people.read_at_locations({new.location}) == []
    assert people.read_at_locations({updated.location}) == [person]
