from pydantic import BaseModel, Field

from app.models.person import PersonRole
from app.runner.config import config


class PersonLocation(BaseModel):
    q: int = Field(ge=0, lt=config.GRID_SIZE)
    r: int = Field(ge=0, lt=config.GRID_SIZE)


class PersonCreate(BaseModel):
    location: PersonLocation
    role: PersonRole
    is_dead: bool
    lifespan: int


class PersonRead(BaseModel):
    id: str
    location: PersonLocation
    role: PersonRole
    is_dead: bool
    lifespan: int
