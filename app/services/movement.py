import random
from dataclasses import dataclass

from app.models.location import Location
from app.models.person import Person
from app.services.building import BuildingService
from app.services.people import PeopleService


@dataclass
class MovementService:
    grid_size: int
    buildings: BuildingService
    people: PeopleService

    def move_people_to_random_adjacent_location(self) -> None:
        for person in self.people.read_many(is_dead=False):
            generated_location = self._generate_random_adjacent_location_for(person)
            reduced_lifespan = person.lifespan - 1
            updated_person = Person(
                id=person.id,
                location=generated_location,
                role=person.role,
                is_dead=reduced_lifespan <= 0,
                lifespan=reduced_lifespan,
            )
            self.people.update_one(updated_person)

    def _generate_random_adjacent_location_for(self, person: Person) -> Location:
        directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        random.shuffle(directions)

        for dq, dr in directions:
            new_q = person.location.q + dq
            new_r = person.location.r + dr

            if not self._is_within_bounds(new_q, new_r):
                continue

            new_location = Location(q=new_q, r=new_r)

            if self._is_location_free(new_location):
                return new_location

        return person.location

    def _is_within_bounds(self, q: int, r: int) -> bool:
        return 0 <= q < self.grid_size and 0 <= r < self.grid_size

    def _is_location_free(self, location: Location) -> bool:
        has_person = self.people.read_many(q=location.q, r=location.r)
        has_building = self.buildings.read_many(q=location.q, r=location.r)

        return not has_person and not has_building
