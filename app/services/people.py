from dataclasses import dataclass

from app.models.person import Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    locations: LocationsInMemoryRepository

    def create_one(self, person: Person) -> Person:
        # Validate location exists before creating person
        self.locations.read_one(person.location_id)
        created = self.people.create_one(person)
        return self._hydrate_person(created)

    def read_all(self) -> list[Person]:
        people = list(self.people)
        return [self._hydrate_person(person) for person in people]

    def read_one(self, person_id: str) -> Person:
        person = self.people.read_one(person_id)
        return self._hydrate_person(person)

    def update_one(self, person: Person) -> None:
        self.people.update_one(person)

    def delete_one(self, person_id: str) -> None:
        self.people.delete_one(person_id)

    def _hydrate_person(self, person: Person) -> Person:
        """Return a Person with its Location object populated."""
        location = self.locations.read_one(person.location_id)
        return Person(
            id=person.id,
            location_id=person.location_id,
            location=location,
        )
