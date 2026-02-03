from dataclasses import dataclass
from typing import Any

from app.models.building import Building
from app.repositories.in_memory.buildings import BuildingsInMemoryRepository


@dataclass
class BuildingService:
    buildings: BuildingsInMemoryRepository

    def create_one(self, building: Building) -> Building:
        return self.buildings.create_one(building)

    def read_one(self, building_id: str) -> Building:
        return self.buildings.read_one(building_id)

    def read_many(self, **filters: Any) -> list[Building]:
        return list(self.buildings.read_many(**filters))

    def delete_one(self, building_id: str) -> None:
        self.buildings.delete_one(building_id)

    def update_one(self, building: Building) -> None:
        self.buildings.update_one(building)
