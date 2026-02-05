import pytest

from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.buildings import BuildingsService
from app.services.initialize import WorldInitializer
from app.services.people import PeopleService


@pytest.fixture
def people_service() -> PeopleService:
    people_repository = PeopleInMemoryRepository()

    return PeopleService(people=people_repository)


@pytest.fixture
def buildings_service() -> BuildingsService:
    buildings_repository = BuildingsInMemoryRepository()

    return BuildingsService(buildings=buildings_repository)


def test_should_not_initialize_when_too_many_entities(
    people_service: PeopleService, buildings_service: BuildingsService
) -> None:
    initializer = WorldInitializer(
        people_service=people_service,
        buildings_service=buildings_service,
        people_amount=1,
        building_amount=1,
        killer_probability=1,
        police_probability=1,
        grid_size=1,
        snapshot_service=None,
    )

    with pytest.raises(ValueError):
        initializer.initialize()


def test_should_initialize(
    people_service: PeopleService, buildings_service: BuildingsService
) -> None:
    initializer = WorldInitializer(
        people_service=people_service,
        buildings_service=buildings_service,
        people_amount=1,
        building_amount=1,
        killer_probability=1,
        police_probability=1,
        grid_size=10,
        snapshot_service=None,
    )
    initializer.initialize()

    people = people_service.read_many()
    buildings = buildings_service.read_many()

    assert len(people) == 1
    assert len(buildings) == 1
