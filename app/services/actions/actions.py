from dataclasses import dataclass, field

from app.models.person import Location, Person
from app.services.actions.strategies import RoleStrategies
from app.services.people import PeopleService


@dataclass
class ActionsService:
    people: PeopleService

    strategies: RoleStrategies = field(default_factory=lambda: RoleStrategies())

    def kill(self) -> None:
        for person in self.people.read_all():
            strategy = self.strategies.get_strategy_for(person.role)
            adjacent_people = self._get_adjacent_people_of(person)
            targets = strategy.get_targets_from(adjacent_people)

            for target in targets:
                self.people.delete_one(target.id)

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
