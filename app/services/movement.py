import random
from dataclasses import dataclass

from app.models.person import Location, Person
from app.services.people import PeopleService


@dataclass
class MovementService:
    grid_size: int
    people: PeopleService

    def move_people_to_random_adjacent_location(self) -> None:
        for person in self.people.read_all():
            generated_location = self._generate_random_adjacent_location_for(person)
            updated_person = Person(id=person.id, location=generated_location)
            self.people.update_one(updated_person)

    def _generate_random_adjacent_location_for(self, person: Person) -> Location:
        adjacent_directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        random.shuffle(adjacent_directions)

        occupied_locations = {
            p.location for p in self.people.read_all() if p.id != person.id
        }

        for dq, dr in adjacent_directions:
            new_q = person.location.q + dq
            new_r = person.location.r + dr

            if not self._is_within_bounds(new_q, new_r):
                continue

            new_location = Location(q=new_q, r=new_r)

            if new_location not in occupied_locations:
                return new_location

        return person.location

    def _is_within_bounds(self, q: int, r: int) -> bool:
        return 0 <= q < self.grid_size and 0 <= r < self.grid_size
