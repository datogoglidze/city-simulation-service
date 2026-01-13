import random
from pathlib import Path

import uvicorn
from typer import Typer

from app.models.person import Person
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
        coordinate_strategy=config.get_coordinate_strategy(),
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
    valid_positions = people.coordinate_strategy.generate_valid_locations(
        config.GRID_SIZE
    )

    random_people = [
        Person(location=random.choice(valid_positions))
        for _ in range(config.PEOPLE_AMOUNT)
    ]

    for person in random_people:
        people.create_one(person)
