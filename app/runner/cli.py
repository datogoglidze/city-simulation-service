import random
from pathlib import Path

import uvicorn
from typer import Typer

from app.models.person import Location, Person
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.repositories.text_file.people_snapshot import PeopleSnapshotJsonRepository
from app.runner.config import config
from app.runner.fastapi import FastApiConfig
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService

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

    initialize_people(people=people_service, snapshot=snapshot_repository)

    uvicorn.run(
        app=FastApiConfig(
            websocket=websocket_manager,
            simulation=SimulationService(
                websocket_manager=websocket_manager,
                snapshot=snapshot_repository,
                people=people_service,
                snapshot_interval=config.SNAPSHOT_INTERVAL,
            ),
            people=people_service,
        ).setup(),
        host=host,
        port=port,
        root_path=root_path,
    )


def initialize_people(
    people: PeopleService,
    snapshot: PeopleSnapshotJsonRepository,
) -> None:
    initial_people = snapshot.load()

    if not initial_people:
        initial_people = [
            Person(
                location=Location(
                    x=random.randint(0, config.GRID_SIZE - 1),
                    y=random.randint(0, config.GRID_SIZE - 1),
                )
            )
            for _ in range(config.PEOPLE_AMOUNT)
        ]

    for person in initial_people:
        people.create_one(person)
