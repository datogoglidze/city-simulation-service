import random
from dataclasses import dataclass

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository


@dataclass
class MovementService:
    grid_size: int
    people: PeopleInMemoryRepository

    def move_to_random_adjacent_location(
        self,
        person: Person,
    ) -> Person:
        adjacent_directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwestm
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        random.shuffle(adjacent_directions)

        occupied_locations = {p.location for p in self.people if p.id != person.id}

        for dq, dr in adjacent_directions:
            new_q = person.location.q + dq
            new_r = person.location.r + dr

            if not self._is_within_bounds(new_q, new_r):
                continue

            new_location = Location(q=new_q, r=new_r)

            if new_location not in occupied_locations:
                return Person(id=person.id, location=new_location)

        return person

    def _is_within_bounds(self, q: int, r: int) -> bool:
        return 0 <= q < self.grid_size and 0 <= r < self.grid_size
