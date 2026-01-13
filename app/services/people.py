import random
from contextlib import suppress
from dataclasses import dataclass

from app.models.errors import DoesNotExistError
from app.models.hex_coordinate import HexCoordinateStrategy
from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    grid_size: int
    coordinate_strategy: HexCoordinateStrategy

    def create_one(self, person: Person) -> Person:
        return self.people.create_one(person)

    def read_all(self) -> list[Person]:
        return list(self.people)

    def read_one(self, person_id: str) -> Person:
        return self.people.read_one(person_id)

    def delete_one(self, person_id: str) -> None:
        self.people.delete_one(person_id)

    def update_location(self) -> None:
        for person in self.people:
            new_location = self._random_neighboring_location(person)
            updated_person = Person(id=person.id, location=new_location)
            with suppress(DoesNotExistError):
                self.people.update_one(updated_person)

    def _random_neighboring_location(self, person: Person) -> Location:
        adjacent_directions = [
            (+1, 0),  # E
            (+1, -1),  # NE
            (0, -1),  # NW
            (-1, 0),  # W
            (-1, +1),  # SW
            (0, +1),  # SE
        ]

        random.shuffle(adjacent_directions)

        for dq, dr in adjacent_directions:
            new_q = person.location.q + dq
            new_r = person.location.r + dr

            if self.coordinate_strategy.is_within_grid_bounds(
                new_q, new_r, self.grid_size
            ):
                return Location(q=new_q, r=new_r)

        return person.location
