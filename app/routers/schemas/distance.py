from pydantic import BaseModel


class DistanceRead(BaseModel):
    distance: int
