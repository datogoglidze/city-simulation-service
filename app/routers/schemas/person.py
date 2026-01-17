from pydantic import BaseModel


class PersonLocation(BaseModel):
    id: str
    q: int
    r: int


class PersonRead(BaseModel):
    id: str
    location: PersonLocation


class PersonCreate(BaseModel):
    location_id: str
