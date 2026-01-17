import pytest

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository


@pytest.fixture
def people() -> PeopleInMemoryRepository:
    return PeopleInMemoryRepository()


@pytest.fixture
def location() -> Location:
    return Location(id="loc1", q=0, r=0, people=[])


@pytest.fixture
def location2() -> Location:
    return Location(id="loc2", q=1, r=1, people=[])


def test_should_read_nothing_when_nothing_exist(
    people: PeopleInMemoryRepository,
) -> None:
    existing_people = people.read_all()

    assert len(existing_people) == 0


def test_should_create_one(
    people: PeopleInMemoryRepository, location: Location
) -> None:
    person = Person(id="1", location=location)

    people.create_one(person)

    assert len(people.read_all()) == 1


def test_should_not_duplicate_on_create_one(
    people: PeopleInMemoryRepository, location: Location
) -> None:
    person = Person(id="1", location=location)
    people.create_one(person)

    with pytest.raises(ExistsError):
        people.create_one(person)


def test_should_not_read_when_does_not_exist(people: PeopleInMemoryRepository) -> None:
    with pytest.raises(DoesNotExistError):
        people.read_one("1")


def test_should_read_one(people: PeopleInMemoryRepository, location: Location) -> None:
    person = Person(id="1", location=location)
    people.create_one(person)

    existing_person = people.read_one("1")

    assert existing_person == person


def test_should_not_delete_when_does_not_exist(
    people: PeopleInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        people.delete_one("1")


def test_should_delete_one(
    people: PeopleInMemoryRepository, location: Location
) -> None:
    person = Person(id="1", location=location)
    people.create_one(person)

    people.delete_one("1")

    assert len(people.read_all()) == 0


def test_should_not_update_when_does_not_exist(
    people: PeopleInMemoryRepository, location: Location
) -> None:
    with pytest.raises(DoesNotExistError):
        people.update_one(Person(id="1", location=location))


def test_should_update_one(
    people: PeopleInMemoryRepository, location: Location, location2: Location
) -> None:
    _person = Person(id="1", location=location)
    people.create_one(_person)
    person = Person(id="1", location=location2)
    people.update_one(person)

    updated_person = people.read_one("1")

    assert updated_person == person
