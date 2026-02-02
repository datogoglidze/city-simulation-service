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
def read_many(
    people: PeopleServiceDependable,
    q: int | None = None,
    r: int | None = None,
    is_dead: bool | None = None,
) -> list[PersonRead]:
    params = {
        "q": q,
        "r": r,
        "is_dead": is_dead,
    }
    params = {key: value for key, value in params.items() if value is not None}
    _people = people.read_many(**params)

    return [
        PersonRead(
            id=person.id,
            location=PersonLocation(
                q=person.location.q,
                r=person.location.r,
            ),
            role=person.role,
            is_dead=person.is_dead,
            lifespan=person.lifespan,
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
        is_dead=_person.is_dead,
        lifespan=_person.lifespan,
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
        is_dead=person.is_dead,
        lifespan=person.lifespan,
    )

    created = people.create_one(_person)

    return PersonRead(
        id=created.id,
        location=PersonLocation(
            q=created.location.q,
            r=created.location.r,
        ),
        role=created.role,
        is_dead=created.is_dead,
        lifespan=created.lifespan,
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
