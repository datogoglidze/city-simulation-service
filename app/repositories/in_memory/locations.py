from dataclasses import dataclass, field
from typing import Iterator

from app.models.errors import DoesNotExistError, ExistsError
from app.models.person import Location


@dataclass
class LocationsInMemoryRepository:
    _locations: dict[str, Location] = field(default_factory=dict)

    def __len__(self) -> int:  # pragma: no cover
        return len(self._locations)

    def __iter__(self) -> Iterator[Location]:  # pragma: no cover
        return iter(self._locations.values())

    def read_all(self) -> list[Location]:
        return list(self._locations.values())

    def read_one(self, location_id: str) -> Location:
        location = self._locations.get(location_id)
        if not location:
            raise DoesNotExistError(location_id)

        return location

    def create_one(self, location: Location) -> Location:
        existing = self._locations.get(location.id)
        if existing:
            raise ExistsError(existing.id)

        self._locations[location.id] = location

        return location

    def update_one(self, location: Location) -> None:
        existing = self._locations.get(location.id)
        if not existing:
            raise DoesNotExistError(location.id)

        self._locations[location.id] = location
