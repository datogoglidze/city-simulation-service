from pathlib import Path

import pytest

from tests.fake import FakePerson

from app.models.person import PersonRole
from app.repositories.text_file.people_snapshot import PeopleSnapshotFileRepository


@pytest.fixture
def snapshot() -> PeopleSnapshotFileRepository:
    return PeopleSnapshotFileRepository(
        snapshot_file=Path("data/test_people_snapshot.json")
    )


def test_should_raise_when_nothing_exist(
    snapshot: PeopleSnapshotFileRepository,
) -> None:
    with pytest.raises(FileNotFoundError):
        snapshot.load()


def test_should_save(
    snapshot: PeopleSnapshotFileRepository,
) -> None:
    person = FakePerson().entity
    snapshot.save([person])

    people = snapshot.load()

    assert len(people) == 1

    snapshot.snapshot_file.unlink()


@pytest.mark.parametrize(
    "person_role",
    [
        PersonRole.citizen,
        PersonRole.killer,
        PersonRole.police,
    ],
)
def test_should_load(
    snapshot: PeopleSnapshotFileRepository, person_role: PersonRole
) -> None:
    person = FakePerson(role=person_role).entity
    snapshot.save([person])

    people = snapshot.load()

    assert people == [person]

    snapshot.snapshot_file.unlink()
