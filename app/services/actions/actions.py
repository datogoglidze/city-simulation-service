from dataclasses import dataclass, field, replace

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
                dead_target = replace(target, is_dead=True)
                self.people.update_one(dead_target)

    def _get_adjacent_people_of(self, person: Person) -> list[Person]:
        directions = [
            (1, 0),  # East
            (1, -1),  # Northeast
            (0, -1),  # Northwest
            (-1, 0),  # West
            (-1, 1),  # Southwest
            (0, 1),  # Southeast
        ]

        adjacent_locations = {
            Location(q=person.location.q + dq, r=person.location.r + dr)
            for dq, dr in directions
        }

        return [
            potential_person
            for potential_person in self.people.read_all()
            if potential_person.location in adjacent_locations
        ]
