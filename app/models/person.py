from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Location:
    id: str
    q: int
    r: int
    people_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Person:
    location_id: str
    id: str = field(default_factory=lambda: str(uuid4()))
