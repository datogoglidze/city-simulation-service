from __future__ import annotations

import random
from dataclasses import dataclass

from app.models.building import Building
from app.models.location import Location
from app.models.person import Person, PersonRole
from app.services.buildings import BuildingsService
from app.services.people import PeopleService
from app.services.snapshot import SnapshotService


@dataclass
class WorldEntities:
    snapshot_service: SnapshotService | None

    grid_size: int

    people_amount: int
    building_amount: int

    killer_probability: float
    police_probability: float

    people_service: PeopleService
    buildings_service: BuildingsService

    def initialize(self) -> None:
        if self.snapshot_service:
            try:
                self.snapshot_service.load_people()
                self.snapshot_service.load_buildings()
                return
            except FileNotFoundError:
                pass

        self._generate_world()

    def _generate_world(self) -> None:
        total_locations = self.grid_size**2
        total_entities = self.people_amount + self.building_amount

        if total_entities > total_locations:
            raise ValueError(
                f"Too many entities to initialize. "
                f"total: {total_entities}, maximum: {total_locations}. "
                f"people: {self.people_amount}, buildings: {self.building_amount}."
            )

        all_locations = [
            Location(q=q, r=r)
            for q in range(self.grid_size)
            for r in range(self.grid_size)
        ]

        sampled_locations = random.sample(all_locations, total_entities)

        building_locations = sampled_locations[: self.building_amount]
        people_locations = sampled_locations[self.building_amount :]

        self._generate_buildings(building_locations)
        self._generate_people(people_locations)

    def _generate_buildings(self, locations: list[Location]) -> None:
        for location in locations:
            self.buildings_service.create_one(Building(location=location))

    def _generate_people(self, locations: list[Location]) -> None:
        for location in locations:
            rand = random.random()

            if rand < self.killer_probability:
                role = PersonRole.killer
            elif rand < self.killer_probability + self.police_probability:
                role = PersonRole.police
            else:
                role = PersonRole.citizen

            self.people_service.create_one(
                Person(
                    location=location,
                    role=role,
                    is_dead=False,
                    lifespan=random.randint(70, 100),
                )
            )
