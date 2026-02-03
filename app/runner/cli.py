from __future__ import annotations

import random
from dataclasses import dataclass

from typer import Typer

from app.models.building import Building
from app.models.location import Location
from app.models.person import Person, PersonRole
from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import buildings, people, simulation
from app.runner.config import config
from app.runner.factory import SnapshotFactory
from app.runner.fastapi import CityApi, UvicornServer
from app.services.actions import ActionsService
from app.services.buildings import BuildingsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService
from app.services.websocket import WebSocketService

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, path: str = "") -> None:
    websocket_manager = WebSocketService()
    buildings_repository = BuildingsInMemoryRepository()
    people_repository = PeopleInMemoryRepository()

    buildings_service = BuildingsService(buildings=buildings_repository)

    people_service = PeopleService(people=people_repository)

    actions_service = ActionsService(people=people_service)

    movement_service = MovementService(
        grid_size=config.GRID_SIZE,
        buildings=buildings_service,
        people=people_service,
    )

    snapshot_service = SnapshotFactory.create(
        snapshot_path=config.SNAPSHOT_PATH,
        snapshot_interval=config.SNAPSHOT_INTERVAL,
        people_service=people_service,
        buildings_service=buildings_service,
    )

    people_initializer = WorldInitializer(
        snapshot_service=snapshot_service,
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
        building_amount=config.BUILDINGS_AMOUNT,
        buildings_service=buildings_service,
        people_service=people_service,
        killer_probability=config.KILLER_PROBABILITY,
        police_probability=config.POLICE_PROBABILITY,
    )

    (
        UvicornServer()
        .with_host(host)
        .and_port(port)
        .on_path(path)
        .before_run(people_initializer.initialize)
        .run(
            CityApi()
            .with_router(simulation.router)
            .with_router(buildings.router)
            .with_router(people.router)
            .with_websocket_manager(websocket_manager)
            .with_simulation_service(
                simulation_service=SimulationService(
                    websocket_manager=websocket_manager,
                    people=people_service,
                    movement=movement_service,
                    actions=actions_service,
                )
            )
            .with_buildings_service(buildings_service)
            .with_people_service(people_service)
            .with_snapshot_service(snapshot_service)
            .build()
        )
    )


@dataclass
class WorldInitializer:
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
