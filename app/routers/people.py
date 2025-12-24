from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from app.models.person import Location, Person
from app.runner.dependencies import get_people_service
from app.services.people import PeopleService

router = APIRouter(prefix="/people", tags=["People"])


class PersonLocation(BaseModel):
    x: int
    y: int


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
def read_all(
    people: PeopleService = Depends(get_people_service),
) -> list[Person]:
    return people.read_all()


@router.get(
    "/{person_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonRead,
)
def read_one(
    person_id: str, people: PeopleService = Depends(get_people_service)
) -> Person:
    person = people.read_one(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(
    person: PersonCreate, people: PeopleService = Depends(get_people_service)
) -> Person:
    _person = Person(Location(**person.location.model_dump()))

    return people.create_one(_person)


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_one(
    person_id: str, people: PeopleService = Depends(get_people_service)
) -> None:
    people.delete_one(person_id)
