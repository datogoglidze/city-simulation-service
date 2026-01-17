from fastapi import APIRouter, HTTPException
from starlette import status

from app.models.errors import DoesNotExistError
from app.models.person import Person
from app.routers.dependables import (
    LocationsServiceDependable,
    MovementServiceDependable,
    PeopleServiceDependable,
)
from app.routers.schemas.distance import DistanceRead
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
                id=person.location.id,
                q=person.location.q,
                r=person.location.r,
            ),
        )
        for person in _people
    ]


@router.get(
    "/distance",
    status_code=status.HTTP_200_OK,
    response_model=DistanceRead,
)
def get_distance(
    person_id_from: str,
    person_id_to: str,
    people: PeopleServiceDependable,
    locations: LocationsServiceDependable,
) -> DistanceRead:
    try:
        person_from = people.read_one(person_id_from)
        person_to = people.read_one(person_id_to)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"{e.resource} with id {e.id} not found"
        )

    distance = locations.get_distance(
        from_q=person_from.location.q,
        from_r=person_from.location.r,
        to_q=person_to.location.q,
        to_r=person_to.location.r,
    )

    return DistanceRead(distance=distance)


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
        raise HTTPException(
            status_code=404, detail=f"{e.resource} with id {e.id} not found"
        )

    return PersonRead(
        id=_person.id,
        location=PersonLocation(
            id=_person.location.id,
            q=_person.location.q,
            r=_person.location.r,
        ),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonRead,
)
def create_one(
    person: PersonCreate,
    people: PeopleServiceDependable,
    locations: LocationsServiceDependable,
    movement: MovementServiceDependable,
) -> PersonRead:
    try:
        location = locations.read_one(person.location_id)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"{e.resource} with id {e.id} not found"
        )

    _person = Person(location=location)
    created = people.create_one(_person)
    movement.add_person_to_location(created)

    return PersonRead(
        id=created.id,
        location=PersonLocation(
            id=created.location.id,
            q=created.location.q,
            r=created.location.r,
        ),
    )


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
        raise HTTPException(
            status_code=404, detail=f"{e.resource} with id {e.id} not found"
        )
