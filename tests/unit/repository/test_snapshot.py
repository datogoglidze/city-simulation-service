from pathlib import Path

import pytest

from app.models.person import Location, Person
from app.repositories.text_file.snapshot import SnapshotJsonRepository


@pytest.fixture
def snapshot() -> SnapshotJsonRepository:
    return SnapshotJsonRepository(snapshot_file=Path("data/test_snapshot.json"))


def test_should_raise_when_nothing_exist(snapshot: SnapshotJsonRepository) -> None:
    # Ensure file doesn't exist from previous test
    if snapshot.snapshot_file.exists():
        snapshot.snapshot_file.unlink()

    with pytest.raises(FileNotFoundError):
        snapshot.load()


def test_should_save(snapshot: SnapshotJsonRepository) -> None:
    location = Location(id="loc1", q=0, r=0, people=[])
    person = Person(id="1", location=location)
    location_with_person = Location(id="loc1", q=0, r=0, people=[person])
    snapshot.save([person], [location_with_person])

    data = snapshot.load()

    assert len(data.people) == 1
    assert len(data.locations) == 1

    snapshot.snapshot_file.unlink()


def test_should_load(snapshot: SnapshotJsonRepository) -> None:
    location = Location(id="loc1", q=0, r=0, people=[])
    person = Person(id="1", location=location)
    location_with_person = Location(id="loc1", q=0, r=0, people=[person])
    snapshot.save([person], [location_with_person])

    data = snapshot.load()

    assert len(data.people) == 1
    assert data.people[0].id == "1"
    assert data.people[0].location.id == "loc1"
    assert len(data.locations) == 1
    assert data.locations[0].id == "loc1"
    assert len(data.locations[0].people) == 1

    snapshot.snapshot_file.unlink()
