from dataclasses import dataclass

from app.models.person import Location, Person, PersonRole
from app.services.people import PeopleService


@dataclass
class ActionsService:
    people: PeopleService

    def kill(self) -> None:
        for person in self.people.read_all():
            if person.role == PersonRole.killer:
                adjacent_people = self._get_adjacent_people_of(person)
                for adjacent_person in adjacent_people:
                    if adjacent_person.role == PersonRole.citizen:
                        self.people.delete_one(adjacent_person.id)

            if person.role == PersonRole.police:
                adjacent_people = self._get_adjacent_people_of(person)
                for adjacent_person in adjacent_people:
                    if adjacent_person.role == PersonRole.killer:
                        self.people.delete_one(adjacent_person.id)

    def _get_adjacent_people_of(self, person: Person) -> list[Person]:
        directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        adjacent_people = []

        for dq, dr in directions:
            adjacent_q = person.location.q + dq
            adjacent_r = person.location.r + dr
            adjacent_location = Location(q=adjacent_q, r=adjacent_r)

            adjacent_people = [
                _person
                for _person in self.people.read_all()
                if _person.location == adjacent_location
            ]

        return adjacent_people
