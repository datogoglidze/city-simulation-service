from pathlib import Path

import pytest

from app.models.person import Location, Person
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository


@pytest.fixture
def snapshot() -> PeopleSnapshotJsonRepository:
    return PeopleSnapshotJsonRepository(
        snapshot_file=Path("data/test_people_snapshot.json")
    )


def test_should_raise_when_nothing_exist(
    snapshot: PeopleSnapshotJsonRepository,
) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot.load()


def test_should_save(
    snapshot: PeopleSnapshotJsonRepository,
) -> None:
    snapshot.save([Person(id="1", location=Location(x=0, y=0))])

    people = snapshot.load()

    assert len(people) == 1

    snapshot.snapshot_file.unlink()


def test_should_load(
    snapshot: PeopleSnapshotJsonRepository,
) -> None:
    snapshot.save([Person(id="1", location=Location(x=0, y=0))])

    people = snapshot.load()

    assert len(people) == 1
    assert people == [Person(id="1", location=Location(x=0, y=0))]

    snapshot.snapshot_file.unlink()
