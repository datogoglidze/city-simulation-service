from fastapi import APIRouter, HTTPException
from starlette import status

from app.models.errors import DoesNotExistError
from app.models.person import Person
from app.routers.dependables import PeopleServiceDependable
from app.routers.schemas.person import PersonCreate, PersonRead

router = APIRouter(prefix="/people", tags=["People"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[PersonRead],
)
def read_all(people: PeopleServiceDependable) -> list[PersonRead]:
    _people = people.read_all()

    return [
        PersonRead(
            id=person.id,
            location_id=person.location_id,
        )
        for person in _people
    ]


@router.get(
    "/{person_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonRead,
)
def read_one(person_id: str, people: PeopleServiceDependable) -> PersonRead:
    try:
        _person = people.read_one(person_id)
    except DoesNotExistError as e:
        raise HTTPException(status_code=404, detail=f"Person with id {e.id} not found")

    return PersonRead(
        id=_person.id,
        location_id=_person.location_id,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(person: PersonCreate, people: PeopleServiceDependable) -> PersonRead:
    _person = Person(location_id=person.location_id)

    created = people.create_one(_person)

    return PersonRead(
        id=created.id,
        location_id=created.location_id,
    )


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_one(person_id: str, people: PeopleServiceDependable) -> None:
    try:
        people.delete_one(person_id)
    except DoesNotExistError as e:
        raise HTTPException(status_code=404, detail=f"Person with id {e.id} not found")
