from dataclasses import dataclass

from app.models.person import Location, Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository


@dataclass
class LocationsService:
    locations: LocationsInMemoryRepository
    people: PeopleInMemoryRepository

    def create_one(self, location: Location) -> Location:
        created = self.locations.create_one(location)
        return self._hydrate_location(created)

    def read_all(self) -> list[Location]:
        locations = list(self.locations)
        return [self._hydrate_location(location) for location in locations]

    def read_one(self, location_id: str) -> Location:
        location = self.locations.read_one(location_id)
        return self._hydrate_location(location)

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

    def _hydrate_location(self, location: Location) -> Location:
        """Return a Location with its People objects populated."""
        people = [
            Person(id=person.id, location_id=person.location_id)
            for person_id in location.people_ids
            if (person := self.people._people.get(person_id)) is not None
        ]
        return Location(
            id=location.id,
            q=location.q,
            r=location.r,
            people_ids=location.people_ids,
            people=people,
        )
