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

    def add_person_to_location(self, location_id: str, person_id: str) -> Location:
        location = self.locations.read_one(location_id)
        updated_location = Location(
            id=location.id,
            q=location.q,
            r=location.r,
            people_ids=tuple([*location.people_ids, person_id]),
        )
        self.locations.update_one(updated_location)
        return updated_location

    def remove_person_from_location(self, location_id: str, person_id: str) -> Location:
        location = self.locations.read_one(location_id)
        updated_people_ids = tuple(
            pid for pid in location.people_ids if pid != person_id
        )
        updated_location = Location(
            id=location.id,
            q=location.q,
            r=location.r,
            people_ids=updated_people_ids,
        )
        self.locations.update_one(updated_location)
        return updated_location

    def move_person(
        self, from_location_id: str, to_location_id: str, person_id: str
    ) -> None:
        self.remove_person_from_location(from_location_id, person_id)
        self.add_person_to_location(to_location_id, person_id)

    def get_adjacent_location_ids(self, location_id: str) -> list[str]:
        """Get IDs of adjacent locations using axial coordinates."""
        location = self.locations.read_one(location_id)

        adjacent_directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        adjacent_ids = []
        all_locations = self.locations.read_all()

        # Create a map of (q, r) -> location_id
        coord_to_id = {(loc.q, loc.r): loc.id for loc in all_locations}

        for dq, dr in adjacent_directions:
            new_q = location.q + dq
            new_r = location.r + dr

            if (new_q, new_r) in coord_to_id:
                adjacent_ids.append(coord_to_id[(new_q, new_r)])

        return adjacent_ids
