from contextlib import suppress
from dataclasses import dataclass

from app.models.errors import DoesNotExistError
from app.models.person import Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.movement import MovementService


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    movement_service: MovementService

    def create_one(self, person: Person) -> Person:
        return self.people.create_one(person)

    def read_all(self) -> list[Person]:
        return list(self.people)

    def read_one(self, person_id: str) -> Person:
        return self.people.read_one(person_id)

    def delete_one(self, person_id: str) -> None:
        self.people.delete_one(person_id)

    def update_locations(self) -> None:
        self.movement_service.occupied_locations = {
            person.location for person in self.people
        }

        for person in self.people:
            moved_person = self.movement_service.move(person)
            with suppress(DoesNotExistError):
                self.people.update_one(moved_person)
