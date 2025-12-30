from pydantic import BaseModel, Field

from app.runner.config import config


class PersonLocation(BaseModel):
    x: int = Field(ge=0, lt=config.GRID_SIZE)
    y: int = Field(ge=0, lt=config.GRID_SIZE)


class PersonCreate(BaseModel):
    location: PersonLocation


class PersonRead(BaseModel):
    id: str
    location: PersonLocation
