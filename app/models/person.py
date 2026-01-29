from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class PersonRole(str, Enum):
    citizen = "citizen"
    killer = "killer"


@dataclass(frozen=True)
class Location:
    q: int
    r: int


@dataclass(frozen=True)
class Person:
    location: Location
    role: PersonRole

    id: str = field(default_factory=lambda: str(uuid4()))
