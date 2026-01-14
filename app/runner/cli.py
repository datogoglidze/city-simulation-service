import random
from pathlib import Path

import uvicorn
from typer import Typer

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.runner.config import config
from app.runner.fastapi import create_app
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, root_path: str = "") -> None:
    websocket_manager = WebSocketManager()

    snapshot_repository = PeopleSnapshotJsonRepository(
        snapshot_file=Path(config.SNAPSHOT_PATH)
    )

    people_service = PeopleService(
        people=PeopleInMemoryRepository(),
        grid_size=config.GRID_SIZE,
    )

    snapshot_service = SnapshotService(
        snapshot_repository=snapshot_repository,
        people_service=people_service,
        interval_seconds=config.SNAPSHOT_INTERVAL,
    )

    try:
        snapshot_service.load_people()
    except FileNotFoundError:
        initialize_people(people_service)

    uvicorn.run(
        app=create_app(
            websocket=websocket_manager,
            simulation_service=SimulationService(
                websocket_manager=websocket_manager,
                people=people_service,
            ),
            snapshot_service=snapshot_service,
            people_service=people_service,
        ),
        host=host,
        port=port,
        root_path=root_path,
    )


def initialize_people(people: PeopleService) -> None:
    grid_size = config.GRID_SIZE
    max_people = grid_size**2

    if config.PEOPLE_AMOUNT > max_people:
        raise ValueError(f"Too many people to initialize. max: {max_people}")

    all_locations = [
        Location(q=q, r=r) for q in range(grid_size) for r in range(grid_size)
    ]

    for location in random.sample(all_locations, config.PEOPLE_AMOUNT):
        people.create_one(Person(location=location))
