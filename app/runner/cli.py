from __future__ import annotations

import random
from dataclasses import dataclass
from uuid import uuid4

from typer import Typer

from app.models.person import Location, Person
from app.repositories.in_memory.locations import LocationsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import locations, people, simulation
from app.runner.config import config
from app.runner.factory import SnapshotFactory
from app.runner.fastapi import CityApi, UvicornServer
from app.runner.websocket import WebSocketManager
from app.services.locations import LocationsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, path: str = "") -> None:
    websocket_manager = WebSocketManager()

    locations_service = LocationsService(locations=LocationsInMemoryRepository())

    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        movement=MovementService(locations_service=locations_service),
        locations=locations_service,
    )

    snapshot_service = SnapshotFactory.create(
        snapshot_path=config.SNAPSHOT_PATH,
        snapshot_interval=config.SNAPSHOT_INTERVAL,
        people_service=people_service,
        locations_service=locations_service,
    )

    city_initializer = CityInitializer(
        snapshot_service=snapshot_service,
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
        people_service=people_service,
        locations_service=locations_service,
    )

    (
        UvicornServer()
        .with_host(host)
        .and_port(port)
        .on_path(path)
        .before_run(city_initializer.initialize)
        .run(
            CityApi()
            .with_router(simulation.router)
            .with_router(people.router)
            .with_router(locations.router)
            .with_websocket_manager(websocket_manager)
            .with_simulation_service(
                simulation_service=SimulationService(
                    websocket_manager=websocket_manager,
                    people=people_service,
                )
            )
            .with_people_service(people_service)
            .with_locations_service(locations_service)
            .with_snapshot_service(snapshot_service)
            .build()
        )
    )


@dataclass
class CityInitializer:
    snapshot_service: SnapshotService | None
    grid_size: int
    people_amount: int
    people_service: PeopleService
    locations_service: LocationsService

    def initialize(self) -> None:
        if self.snapshot_service:
            try:
                self.snapshot_service.load_snapshot()
            except FileNotFoundError:
                self._generate_city()
        else:
            self._generate_city()

    def _generate_city(self) -> None:
        """Generate all locations and randomly place people."""
        max_people = self.grid_size**2

        if self.people_amount > max_people:
            raise ValueError(f"Too many people to initialize. max: {max_people}")

        # Create all locations
        all_location_ids = []
        for q in range(self.grid_size):
            for r in range(self.grid_size):
                location_id = str(uuid4())
                location = Location(id=location_id, q=q, r=r, people_ids=tuple())
                self.locations_service.create_one(location)
                all_location_ids.append(location_id)

        # Randomly assign people to locations
        selected_location_ids = random.sample(all_location_ids, self.people_amount)
        for location_id in selected_location_ids:
            person = Person(location_id=location_id)
            self.people_service.create_one(person)
