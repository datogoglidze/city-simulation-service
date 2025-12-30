from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette import status

from app.models.errors import DoesNotExistError
from app.models.person import Location, Person
from app.routers.dependables import PeopleServiceDependable
from app.runner.config import config

router = APIRouter(prefix="/people", tags=["People"])


class PersonLocation(BaseModel):
    x: int = Field(ge=0, lt=config.GRID_SIZE)
    y: int = Field(ge=0, lt=config.GRID_SIZE)


class PersonCreate(BaseModel):
    location: PersonLocation


class PersonRead(BaseModel):
    id: str
    location: PersonLocation


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
                x=person.location.x,
                y=person.location.y,
            ),
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
            x=_person.location.x,
            y=_person.location.y,
        ),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(person: PersonCreate, people: PeopleServiceDependable) -> PersonRead:
    _person = Person(
        location=Location(
            x=person.location.x,
            y=person.location.y,
        )
    )

    created = people.create_one(_person)

    return PersonRead(
        id=created.id,
        location=PersonLocation(
            x=created.location.x,
            y=created.location.y,
        ),
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
