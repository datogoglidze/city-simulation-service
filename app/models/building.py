from dataclasses import dataclass, field
from uuid import uuid4

from app.models.location import Location


@dataclass(frozen=True)
class Building:
    location: Location

    id: str = field(default_factory=lambda: str(uuid4()))
