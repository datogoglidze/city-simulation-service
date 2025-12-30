from pathlib import Path

import uvicorn
from typer import Typer

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
        snapshot=snapshot_repository,
        grid_size=config.GRID_SIZE,
        people_amount=config.PEOPLE_AMOUNT,
    )

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
