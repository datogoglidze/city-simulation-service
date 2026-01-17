import random
from contextlib import suppress
from dataclasses import dataclass

from app.models.errors import DoesNotExistError
from app.models.person import Location, Person
from app.services.locations import LocationsService
from app.services.people import PeopleService


@dataclass
class MovementService:
    people_service: PeopleService
    locations_service: LocationsService

    def move_person_to_location(self, person: Person, new_location_id: str) -> None:
        if person.location_id == new_location_id:
            return

        self.remove_person_from_location(person)
        self.add_person_to_location(person)

        moved_person = Person(id=person.id, location_id=new_location_id)
        self.people_service.update_one(moved_person)

    def add_person_to_location(self, person: Person) -> None:
        location = self.locations_service.read_one(person.location_id)
        updated_location = Location(
            id=location.id,
            q=location.q,
            r=location.r,
            people_ids=[*location.people_ids, person.id],
        )
        self.locations_service.update_one(updated_location)

    def remove_person_from_location(self, person: Person) -> None:
        location = self.locations_service.read_one(person.location_id)
        updated_location = Location(
            id=location.id,
            q=location.q,
            r=location.r,
            people_ids=[pid for pid in location.people_ids if pid != person.id],
        )
        self.locations_service.update_one(updated_location)

    def move_all_people_randomly(self) -> None:
        for person in self.people_service.read_all():
            with suppress(DoesNotExistError):
                new_location = self._pick_random_adjacent_location(person)
                if new_location:
                    self.move_person_to_location(person, new_location.id)

    def _pick_random_adjacent_location(self, person: Person) -> Location | None:
        adjacent_locations = self.locations_service.get_adjacent_locations(
            person.location_id
        )

        available_locations = [
            location
            for location in adjacent_locations
            if len(self.locations_service.read_one(location.id).people_ids) == 0
        ]

        if not available_locations:
            return None

        return random.choice(available_locations)
