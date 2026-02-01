import pytest

from tests.fake import FakePerson

from app.models.person import Location, Person
from app.repositories.in_memory.indexes import _FieldIndex


@pytest.fixture
def location_index() -> _FieldIndex[Person, Location, str]:
    return _FieldIndex(key_extractor=lambda person: person.location)


def test_should_add_location(
    location_index: _FieldIndex[Person, Location, str],
) -> None:
    person = FakePerson().entity
    location_index.create_one(entity_id=person.id, entity=person)

    result = location_index.read_one(person.location)

    assert result == {person.id}


def test_should_remove_location(
    location_index: _FieldIndex[Person, Location, str],
) -> None:
    person = FakePerson().entity
    location_index.create_one(person.id, person)
    location_index.delete_one(person.id, person)

    result = location_index.read_one(person.location)

    assert result == set()


def test_should_update_location(
    location_index: _FieldIndex[Person, Location, str],
) -> None:
    new = FakePerson().entity
    updated = FakePerson().entity
    person = Person(
        id=new.id,
        location=updated.location,
        role=new.role,
        is_dead=new.is_dead,
        lifespan=new.lifespan,
    )

    location_index.create_one(new.id, new)
    location_index.update_one(new.id, new, person)

    assert location_index.read_one(new.location) == set()
    assert location_index.read_one(updated.location) == {new.id}
