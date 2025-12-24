from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.models.person import Location, Person
from app.runner.dependencies import get_people_service
from app.services.people import PeopleService

router = APIRouter(prefix="/people", tags=["People"])


class PersonLocation(BaseModel):
    x: int
    y: int


class PersonCreate(BaseModel):
    location: PersonLocation


@router.get("")
def read_all(
    people: PeopleService = Depends(get_people_service),
) -> list[Person]:
    return people.read_all()


@router.get("/{person_id}")
def read_one(
    person_id: str, people: PeopleService = Depends(get_people_service)
) -> Person:
    person = people.read_one(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@router.post("")
def create_one(
    person: PersonCreate, people: PeopleService = Depends(get_people_service)
) -> Person:
    _person = Person(Location(**person.location.model_dump()))

    return people.create_one(_person)


@router.delete("/{person_id}")
def delete_one(
    person_id: str, people: PeopleService = Depends(get_people_service)
) -> None:
    people.delete_one(person_id)
