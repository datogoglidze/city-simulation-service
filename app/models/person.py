from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Location:
    q: int
    r: int
    people_ids: list[str] = field(default_factory=list)

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True)
class Person:
    location_id: str

    id: str = field(default_factory=lambda: str(uuid4()))
