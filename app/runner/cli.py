from __future__ import annotations

import random
from dataclasses import dataclass

import uvicorn
from typer import Typer

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.runner.config import config
from app.runner.factory import SnapshotFactory
from app.runner.fastapi import create_app
from app.runner.websocket import WebSocketManager
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, root_path: str = "") -> None:
    websocket_manager = WebSocketManager()

    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        movement=MovementService(grid_size=config.GRID_SIZE),
    )

    snapshot_service = SnapshotFactory.create(
        snapshot_path=config.SNAPSHOT_PATH,
        snapshot_interval=config.SNAPSHOT_INTERVAL,
        people_service=people_service,
    )

    PeopleInitializer(
        snapshot_service=snapshot_service,
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
    ).initialize(people_service)

    uvicorn.run(
        app=create_app(
            websocket=websocket_manager,
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
            ),
            people_service=people_service,
            snapshot_service=snapshot_service,
        ),
        host=host,
        port=port,
        root_path=root_path,
    )


@dataclass
class PeopleInitializer:
    snapshot_service: SnapshotService | None
    grid_size: int
    people_amount: int

    def initialize(self, people: PeopleService) -> None:
        if self.snapshot_service:
            try:
                self.snapshot_service.load_people()
            except FileNotFoundError:
                self._generate_people(people)
        else:
            self._generate_people(people)

    def _generate_people(self, people: PeopleService) -> None:
        max_people = self.grid_size**2

        if self.people_amount > max_people:
            raise ValueError(f"Too many people to initialize. max: {max_people}")

        all_locations = [
            Location(q=q, r=r)
            for q in range(self.grid_size)
            for r in range(self.grid_size)
        ]

        for location in random.sample(all_locations, self.people_amount):
            people.create_one(Person(location=location))
