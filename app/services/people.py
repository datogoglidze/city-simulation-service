from dataclasses import dataclass

from app.models.person import Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    locations: LocationsInMemoryRepository

    def create_one(self, person: Person) -> Person:
        self.locations.read_one(person.location.id)
        created = self.people.create_one(person)
        return created

    def read_all(self) -> list[Person]:
        return list(self.people)

    def read_one(self, person_id: str) -> Person:
        return self.people.read_one(person_id)

    def update_one(self, person: Person) -> None:
        self.people.update_one(person)

    def delete_one(self, person_id: str) -> None:
        self.people.delete_one(person_id)
