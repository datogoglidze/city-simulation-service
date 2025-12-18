from fastapi import APIRouter, Depends

from app.core.people import PeopleService
from app.core.person import Person
from app.runner.dependencies import get_people_service

router = APIRouter(prefix="/people", tags=["People"])


@router.get("/")
def get_people(
    people: PeopleService = Depends(get_people_service),
) -> list[Person]:
    return people.get_all()
