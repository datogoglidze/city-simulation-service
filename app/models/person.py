from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Location:
    x: int
    y: int


@dataclass
class Person:
    location: Location

    id: str = field(default_factory=lambda: str(uuid4()))
