from dataclasses import dataclass
from functools import cached_property
from typing import Any

from faker import Faker

from app.models.person import Location, Person, PersonRole


@dataclass(frozen=True)
class FakePerson:
    faker: Faker = Faker()
    role: PersonRole | None = None
    location: Location | None = None
    is_dead: bool | None = None

    @cached_property
    def entity(self) -> Person:
        return Person(
            location=(
                self.location
                or Location(
                    q=self.faker.random_int(min=0, max=10),
                    r=self.faker.random_int(min=0, max=10),
                )
            ),
            role=self.role or PersonRole.citizen,
            is_dead=self.is_dead or False,
        )

    def json(self) -> dict[str, Any]:
        return {
            "location": {
                "q": self.entity.location.q,
                "r": self.entity.location.r,
            },
            "role": self.entity.role.value,
            "is_dead": self.entity.is_dead,
        }
