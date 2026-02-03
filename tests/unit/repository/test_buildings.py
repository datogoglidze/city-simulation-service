import pytest

from tests.fake import FakeBuilding

from app.models.building import Building
from app.models.errors import DoesNotExistError, ExistsError
from app.repositories.in_memory.buildings import BuildingsInMemoryRepository


@pytest.fixture
def buildings() -> BuildingsInMemoryRepository:
    return BuildingsInMemoryRepository()


def test_should_read_nothing_when_nothing_exist(
    buildings: BuildingsInMemoryRepository,
) -> None:
    existing_buildings = buildings

    assert len(existing_buildings) == 0


def test_should_create_one(buildings: BuildingsInMemoryRepository) -> None:
    building = FakeBuilding().entity

    buildings.create_one(building)

    assert len(buildings) == 1


def test_should_not_duplicate_on_create_one(
    buildings: BuildingsInMemoryRepository,
) -> None:
    building = FakeBuilding().entity
    buildings.create_one(building)

    with pytest.raises(ExistsError):
        buildings.create_one(building)


def test_should_not_read_when_does_not_exist(
    buildings: BuildingsInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        buildings.read_one(FakeBuilding().entity.id)


def test_should_read_one(buildings: BuildingsInMemoryRepository) -> None:
    building = FakeBuilding().entity
    buildings.create_one(building)

    existing_building = buildings.read_one(building.id)

    assert existing_building == building


def test_should_not_delete_when_does_not_exist(
    buildings: BuildingsInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        buildings.delete_one(FakeBuilding().entity.id)


def test_should_delete_one(buildings: BuildingsInMemoryRepository) -> None:
    building = FakeBuilding().entity
    buildings.create_one(building)

    buildings.delete_one(building.id)

    assert len(buildings) == 0


def test_should_not_update_when_does_not_exist(
    buildings: BuildingsInMemoryRepository,
) -> None:
    with pytest.raises(DoesNotExistError):
        buildings.update_one(FakeBuilding().entity)


def test_should_update_one(buildings: BuildingsInMemoryRepository) -> None:
    new = FakeBuilding().entity
    created = buildings.create_one(new)
    updated = FakeBuilding().entity
    building = Building(id=new.id, location=updated.location)
    buildings.update_one(building)

    updated_building = buildings.read_one(created.id)

    assert updated_building == building


def test_should_read_many_with_no_filters(
    buildings: BuildingsInMemoryRepository,
) -> None:
    building = FakeBuilding().entity
    buildings.create_one(building)

    assert list(buildings.read_many()) == [building]


def test_should_not_read_many_with_unknown_filter(
    buildings: BuildingsInMemoryRepository,
) -> None:
    with pytest.raises(ValueError, match="Unknown filter <unknown_filter>"):
        buildings.read_many(unknown_filter="value")


def test_should_read_many(buildings: BuildingsInMemoryRepository) -> None:
    building = FakeBuilding().entity
    buildings.create_one(building)

    assert list(buildings.read_many(q=building.location.q, r=building.location.r)) == [
        building
    ]
