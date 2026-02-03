from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.models.building import Building
from app.models.errors import DoesNotExistError
from app.models.location import Location
from app.routers.dependables import BuildingsServiceDependable
from app.routers.schemas.building import (
    BuildingCreate,
    BuildingFilters,
    BuildingLocation,
    BuildingRead,
)

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[BuildingRead],
)
def read_many(
    buildings: BuildingsServiceDependable, params: BuildingFilters = Depends()
) -> list[BuildingRead]:
    filters = params.model_dump(exclude_none=True)

    _buildings = buildings.read_many(**filters)

    return [
        BuildingRead(
            id=building.id,
            location=BuildingLocation(q=building.location.q, r=building.location.r),
        )
        for building in _buildings
    ]


@router.get(
    "/{building_id}",
    status_code=status.HTTP_200_OK,
    response_model=BuildingRead,
)
def read_one(building_id: str, buildings: BuildingsServiceDependable) -> BuildingRead:
    try:
        _building = buildings.read_one(building_id)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"Building with id {e.id} not found"
        )

    return BuildingRead(
        id=_building.id,
        location=BuildingLocation(q=_building.location.q, r=_building.location.r),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BuildingRead,
)
def create_one(
    building: BuildingCreate, buildings: BuildingsServiceDependable
) -> BuildingRead:
    _building = Building(
        location=Location(q=building.location.q, r=building.location.r),
    )

    created = buildings.create_one(_building)

    return BuildingRead(
        id=created.id,
        location=BuildingLocation(q=created.location.q, r=created.location.r),
    )


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_one(building_id: str, buildings: BuildingsServiceDependable) -> None:
    try:
        buildings.delete_one(building_id)
    except DoesNotExistError as e:
        raise HTTPException(
            status_code=404, detail=f"Building with id {e.id} not found"
        )
