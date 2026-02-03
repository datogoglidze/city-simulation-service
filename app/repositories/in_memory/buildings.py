from dataclasses import dataclass, field
from typing import Any, Iterator

from app.models.building import Building
from app.models.errors import DoesNotExistError, ExistsError
from app.repositories.in_memory.indexes import IndexManager


@dataclass
class BuildingsInMemoryRepository:
    _buildings: dict[str, Building] = field(default_factory=dict)

    indexes: IndexManager[Building, str] = field(
        default_factory=lambda: IndexManager(
            extractors={
                "q": lambda building: building.location.q,
                "r": lambda building: building.location.r,
            }
        )
    )

    def __len__(self) -> int:  # pragma: no cover
        return len(self._buildings)

    def __iter__(self) -> Iterator[Building]:  # pragma: no cover
        return iter(self._buildings.values())

    def read_one(self, building_id: str) -> Building:
        building = self._buildings.get(building_id)
        if not building:
            raise DoesNotExistError(building_id)

        return building

    def create_one(self, building: Building) -> Building:
        existing = self._buildings.get(building.id)
        if existing:
            raise ExistsError(existing.id)

        self._buildings[building.id] = building
        self.indexes.create_one(building.id, building)

        return building

    def delete_one(self, building_id: str) -> None:
        building = self._buildings.get(building_id)
        if not building:
            raise DoesNotExistError(building_id)

        self.indexes.delete_one(building_id, building)
        self._buildings.pop(building_id, None)

    def update_one(self, building: Building) -> None:
        existing = self._buildings.get(building.id)
        if not existing:
            raise DoesNotExistError(building.id)

        self.indexes.update_one(building.id, existing, building)
        self._buildings[building.id] = building

    def read_many(self, **filters: Any) -> Iterator[Building]:
        if not filters:
            return iter(self._buildings.values())

        building_ids = self.indexes.read_many(**filters)

        buildings = []
        for building_id in building_ids:
            building = self._buildings.get(building_id)
            if building is not None:
                buildings.append(building)

        return iter(buildings)
