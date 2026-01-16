import random
from dataclasses import dataclass

from app.models.person import Person
from app.services.locations import LocationsService


@dataclass
class MovementService:
    locations_service: LocationsService

    def move_to_random_adjacent_location(self, person: Person) -> Person:
        """Move person to a random adjacent location if available."""
        adjacent_location_ids = self.locations_service.get_adjacent_location_ids(
            person.location_id
        )

        # Filter out occupied locations
        available_location_ids = [
            loc_id
            for loc_id in adjacent_location_ids
            if len(self.locations_service.read_one(loc_id).people_ids) == 0
        ]

        if not available_location_ids:
            return person

        # Pick a random available location
        new_location_id = random.choice(available_location_ids)

        return Person(id=person.id, location_id=new_location_id)
