from pydantic import BaseModel, Field

from app.runner.config import config


class BuildingLocation(BaseModel):
    q: int = Field(ge=0, lt=config.GRID_SIZE)
    r: int = Field(ge=0, lt=config.GRID_SIZE)


class BuildingCreate(BaseModel):
    location: BuildingLocation


class BuildingRead(BaseModel):
    id: str
    location: BuildingLocation


class BuildingFilters(BaseModel):
    q: int | None = None
    r: int | None = None
