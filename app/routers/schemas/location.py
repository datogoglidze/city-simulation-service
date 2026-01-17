from pydantic import BaseModel


class LocationPerson(BaseModel):
    id: str


class LocationRead(BaseModel):
    id: str
    q: int
    r: int
    people: list[LocationPerson]
