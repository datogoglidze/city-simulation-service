from fastapi import APIRouter, HTTPException
from starlette import status

from app.models.errors import DoesNotExistError
from app.models.person import Location, Person
from app.routers.dependables import PeopleServiceDependable
from app.routers.schemas.person import PersonCreate, PersonLocation, PersonRead

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
            location=PersonLocation(
                q=person.location.q,
                r=person.location.r,
            ),
            role=person.role,
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
        location=PersonLocation(
            q=_person.location.q,
            r=_person.location.r,
        ),
        role=_person.role,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(person: PersonCreate, people: PeopleServiceDependable) -> PersonRead:
    _person = Person(
        location=Location(
            q=person.location.q,
            r=person.location.r,
        ),
        role=person.role,
    )

    created = people.create_one(_person)

    return PersonRead(
        id=created.id,
        location=PersonLocation(
            q=created.location.q,
            r=created.location.r,
        ),
        role=created.role,
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
