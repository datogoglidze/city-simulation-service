from pydantic import BaseModel


class LocationRead(BaseModel):
    id: str
    q: int
    r: int
    people_ids: list[str]
