from dataclasses import dataclass
from functools import cached_property
from typing import Any

from faker import Faker

from app.models.person import Location, Person, PersonRoles


@dataclass(frozen=True)
class FakePerson:
    faker: Faker = Faker()
    role: PersonRoles | None = None
    location: Location | None = None

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
            role=self.role or PersonRoles.citizen,
        )

    def json(self) -> dict[str, Any]:
        return {
            "location": {
                "q": self.entity.location.q,
                "r": self.entity.location.r,
            },
            "role": self.entity.role.value,
        }
