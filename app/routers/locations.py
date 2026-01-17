from fastapi import APIRouter, HTTPException
from starlette import status

from app.models.errors import DoesNotExistError
from app.routers.dependables import LocationsServiceDependable
from app.routers.schemas.location import LocationPerson, LocationRead

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[LocationRead],
)
def read_all(locations: LocationsServiceDependable) -> list[LocationRead]:
    _locations = locations.read_all()

    return [
        LocationRead(
            id=location.id,
            q=location.q,
            r=location.r,
            people=[LocationPerson(id=person.id) for person in location.people],
        )
        for location in _locations
    ]


@router.get(
    "/{location_id}",
    status_code=status.HTTP_200_OK,
    response_model=LocationRead,
)
def read_one(
    location_id: str,
    locations: LocationsServiceDependable,
) -> LocationRead:
    try:
        _location = locations.read_one(location_id)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"Location with id {e.id} not found"
        )

    return LocationRead(
        id=_location.id,
        q=_location.q,
        r=_location.r,
        people=[LocationPerson(id=person.id) for person in _location.people],
    )
