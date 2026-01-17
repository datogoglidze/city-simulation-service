from dataclasses import dataclass

from app.models.person import Location
from app.repositories.in_memory.locations import LocationsInMemoryRepository


@dataclass
class LocationsService:
    locations: LocationsInMemoryRepository

    def create_one(self, location: Location) -> Location:
        return self.locations.create_one(location)

    def read_all(self) -> list[Location]:
        return list(self.locations)

    def read_one(self, location_id: str) -> Location:
        return self.locations.read_one(location_id)

    def update_one(self, location: Location) -> None:
        self.locations.update_one(location)

    def get_adjacent_locations(self, location_id: str) -> list[Location]:
        location = self.locations.read_one(location_id)

        adjacent_directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        adjacent_ids: list[Location] = []

        coord_to_id = {
            (location.q, location.r): location for location in self.locations
        }

        for dq, dr in adjacent_directions:
            new_q = location.q + dq
            new_r = location.r + dr

            if (new_q, new_r) in coord_to_id:
                adjacent_ids.append(coord_to_id[(new_q, new_r)])

        return adjacent_ids
