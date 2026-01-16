from pydantic import BaseModel


class PersonCreate(BaseModel):
    location_id: str


class PersonRead(BaseModel):
    id: str
    location_id: str
