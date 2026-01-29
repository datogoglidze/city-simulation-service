from __future__ import annotations

import random
from dataclasses import dataclass

from typer import Typer

from app.models.person import Location, Person, PersonRoles
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import people, simulation
from app.runner.config import config
from app.runner.factory import SnapshotFactory
from app.runner.fastapi import CityApi, UvicornServer
from app.runner.websocket import WebSocketManager
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, path: str = "") -> None:
    websocket_manager = WebSocketManager()
    people_repository = PeopleInMemoryRepository()

    people_service = PeopleService(people=people_repository)

    movement_service = MovementService(
        grid_size=config.GRID_SIZE, people=people_service
    )

    snapshot_service = SnapshotFactory.create(
        snapshot_path=config.SNAPSHOT_PATH,
        snapshot_interval=config.SNAPSHOT_INTERVAL,
        people_service=people_service,
    )

    people_initializer = PeopleInitializer(
        snapshot_service=snapshot_service,
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
        people_service=people_service,
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
            .with_router(people.router)
            .with_websocket_manager(websocket_manager)
            .with_simulation_service(
                simulation_service=SimulationService(
                    websocket_manager=websocket_manager,
                    people=people_service,
                    movement=movement_service,
                )
            )
            .with_people_service(people_service)
            .with_snapshot_service(snapshot_service)
            .build()
        )
    )


@dataclass
class PeopleInitializer:
    snapshot_service: SnapshotService | None
    grid_size: int
    people_amount: int
    people_service: PeopleService

    def initialize(self) -> None:
        if self.snapshot_service:
            try:
                self.snapshot_service.load_people()
            except FileNotFoundError:
                self._generate_people()
        else:
            self._generate_people()

    def _generate_people(self) -> None:
        max_people = self.grid_size**2

        if self.people_amount > max_people:
            raise ValueError(f"Too many people to initialize. max: {max_people}")

        all_locations = [
            Location(q=q, r=r)
            for q in range(self.grid_size)
            for r in range(self.grid_size)
        ]

        for location in random.sample(all_locations, self.people_amount):
            self.people_service.create_one(
                Person(location=location, role=PersonRoles.citizen)
            )
