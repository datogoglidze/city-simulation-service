from fastapi import APIRouter, HTTPException
from starlette import status

from app.models.errors import DoesNotExistError
from app.models.person import Person
from app.routers.dependables import (
    MovementServiceDependable,
    PeopleServiceDependable,
)
from app.routers.schemas.person import PersonCreate, PersonLocation, PersonRead

router = APIRouter(prefix="/people", tags=["People"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[PersonRead],
)
def read_all(people: PeopleServiceDependable) -> list[PersonRead]:
    _people = people.read_all()

    return [_person_to_schema(person) for person in _people]


@router.get(
    "/{person_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonRead,
)
def read_one(
    person_id: str,
    people: PeopleServiceDependable,
) -> PersonRead:
    try:
        _person = people.read_one(person_id)
    except DoesNotExistError as e:
        raise HTTPException(status_code=404, detail=f"Person with id {e.id} not found")

    return _person_to_schema(_person)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(
    person: PersonCreate,
    people: PeopleServiceDependable,
    movement: MovementServiceDependable,
) -> PersonRead:
    _person = Person(location_id=person.location_id)

    try:
        created = people.create_one(_person)
        movement.add_person_to_location(created)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"Location with id {e.id} not found"
        )

    return _person_to_schema(created)


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_one(
    person_id: str,
    people: PeopleServiceDependable,
    movement: MovementServiceDependable,
) -> None:
    try:
        person = people.read_one(person_id)
        movement.remove_person_from_location(person)
        people.delete_one(person_id)
    except DoesNotExistError as e:
        raise HTTPException(status_code=404, detail=f"Person with id {e.id} not found")


def _person_to_schema(person: Person) -> PersonRead:
    if not person.location:
        raise ValueError(f"Person {person.id} has no location populated")

    return PersonRead(
        id=person.id,
        location=PersonLocation(
            id=person.location.id,
            q=person.location.q,
            r=person.location.r,
        ),
    )
