from contextlib import suppress
from dataclasses import dataclass

from app.models.errors import DoesNotExistError
from app.models.person import Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.services.locations import LocationsService
from app.services.movement import MovementService


@dataclass
class PeopleService:
    people: PeopleInMemoryRepository
    movement: MovementService
    locations: LocationsService

    def create_one(self, person: Person) -> Person:
        created_person = self.people.create_one(person)
        # Add person to their location
        self.locations.add_person_to_location(person.location_id, person.id)
        return created_person

    def read_all(self) -> list[Person]:
        return list(self.people)

    def read_one(self, person_id: str) -> Person:
        return self.people.read_one(person_id)

    def delete_one(self, person_id: str) -> None:
        person = self.people.read_one(person_id)
        # Remove person from their location
        self.locations.remove_person_from_location(person.location_id, person.id)
        self.people.delete_one(person_id)

    def update_locations(self) -> None:
        """Move all people to random adjacent locations."""
        for person in self.people:
            moved_person = self.movement.move_to_random_adjacent_location(person)

            with suppress(DoesNotExistError):
                if moved_person.location_id != person.location_id:
                    # Update location tracking
                    self.locations.move_person(
                        person.location_id, moved_person.location_id, person.id
                    )
                    # Update person
                    self.people.update_one(moved_person)
