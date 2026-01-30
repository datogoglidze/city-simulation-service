from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.models.person import Person, PersonRole


class RoleStrategy(ABC):  # pragma: no cover
    @abstractmethod
    def get_targets_from(self, adjacent_people: list[Person]) -> list[Person]:
        pass


class CitizenStrategy(RoleStrategy):
    def get_targets_from(self, adjacent_people: list[Person]) -> list[Person]:
        return []


class KillerStrategy(RoleStrategy):
    def get_targets_from(self, adjacent_people: list[Person]) -> list[Person]:
        return [
            person for person in adjacent_people if person.role == PersonRole.citizen
        ]


class PoliceStrategy(RoleStrategy):
    def get_targets_from(self, adjacent_people: list[Person]) -> list[Person]:
        return [
            person for person in adjacent_people if person.role == PersonRole.killer
        ]


@dataclass
class RoleStrategies:
    strategies: dict[PersonRole, RoleStrategy] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.register_strategy_for(role=PersonRole.citizen, strategy=CitizenStrategy())
        self.register_strategy_for(role=PersonRole.killer, strategy=KillerStrategy())
        self.register_strategy_for(role=PersonRole.police, strategy=PoliceStrategy())

    def get_strategy_for(self, role: PersonRole) -> RoleStrategy:
        return self.strategies[role]

    def register_strategy_for(self, role: PersonRole, strategy: RoleStrategy) -> None:
        self.strategies[role] = strategy
