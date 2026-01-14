import random
from dataclasses import dataclass, field

from app.models.person import Location, Person


@dataclass
class MovementService:
    grid_size: int
    occupied_locations: set[Location] = field(default_factory=set)

    def move(self, person: Person) -> Person:
        new_location = self._calculate_next_location(current_location=person.location)
        if new_location != person.location:
            self.occupied_locations.discard(person.location)
        self.occupied_locations.add(new_location)

        return Person(id=person.id, location=new_location)

    def _calculate_next_location(self, current_location: Location) -> Location:
        adjacent_directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        random.shuffle(adjacent_directions)

        for dq, dr in adjacent_directions:
            new_q = current_location.q + dq
            new_r = current_location.r + dr

            if not self._is_within_bounds(new_q, new_r):
                continue

            new_location = Location(q=new_q, r=new_r)

            if new_location not in self.occupied_locations:
                return new_location

        return current_location

    def _is_within_bounds(self, q: int, r: int) -> bool:
        return 0 <= q < self.grid_size and 0 <= r < self.grid_size
