from __future__ import annotations

from typer import Typer

from app.repositories.in_memory.buildings import BuildingsInMemoryRepository
from app.repositories.in_memory.people import PeopleInMemoryRepository
from app.routers import buildings, people, simulation
from app.runner.config import config
from app.runner.factory import JsonFileRepository
from app.runner.fastapi import CityApi, UvicornServer
from app.services.actions import ActionsService
from app.services.buildings import BuildingsService
from app.services.movement import MovementService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService
from app.services.websocket import WebSocketService
from app.services.world_entities import WorldEntities

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

    snapshot_service: SnapshotService | None = None

    if config.SNAPSHOT_PATH:
        if not config.SNAPSHOT_INTERVAL:
            raise ValueError("SNAPSHOT_INTERVAL is required when SNAPSHOT_PATH is set")

        json_repository = JsonFileRepository(snapshot_path=config.SNAPSHOT_PATH)

        snapshot_service = SnapshotService(
            people_snapshot_repository=json_repository.people(),
            buildings_snapshot_repository=json_repository.buildings(),
            people_service=people_service,
            buildings_service=buildings_service,
            interval_seconds=int(config.SNAPSHOT_INTERVAL),
        )

    world_entities = WorldEntities(
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
        .before_run(world_entities.initialize)
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
