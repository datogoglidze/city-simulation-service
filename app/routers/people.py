from fastapi import APIRouter, Depends

from app.core.people import PeopleService
from app.core.person import Person
from app.routers.dependencies import get_people_service

router = APIRouter(prefix="/people", tags=["People"])


@router.get("/")
def get_people(
    service: PeopleService = Depends(get_people_service),
) -> list[Person]:
    return service.get_all()
