from fastapi import APIRouter, Depends

from app.models.person import Person
from app.runner.dependencies import get_people_service
from app.services.people import PeopleService

router = APIRouter(prefix="/people", tags=["People"])


@router.get("/")
def get_people(
    people: PeopleService = Depends(get_people_service),
) -> list[Person]:
    return people.get_all()
