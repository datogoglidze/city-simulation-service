from pathlib import Path

import pytest

from app.models.person import Location, Person
from app.repositories.text_file.snapshot import SnapshotJsonRepository


@pytest.fixture
def snapshot() -> SnapshotJsonRepository:
    return SnapshotJsonRepository(snapshot_file=Path("data/test_snapshot.json"))


def test_should_raise_when_nothing_exist(snapshot: SnapshotJsonRepository) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot.load()


def test_should_save(snapshot: SnapshotJsonRepository) -> None:
    person = Person(id="1", location_id="loc1")
    location = Location(id="loc1", q=0, r=0, people_ids=["1"])
    snapshot.save([person], [location])

    data = snapshot.load()

    assert len(data.people) == 1
    assert len(data.locations) == 1

    snapshot.snapshot_file.unlink()


def test_should_load(snapshot: SnapshotJsonRepository) -> None:
    person = Person(id="1", location_id="loc1")
    location = Location(id="loc1", q=0, r=0, people_ids=["1"])
    snapshot.save([person], [location])

    data = snapshot.load()

    assert data.people == [person]
    assert data.locations == [location]

    snapshot.snapshot_file.unlink()
