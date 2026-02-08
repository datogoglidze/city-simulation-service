from __future__ import annotations

from typer import Typer

from app.routers import buildings, people, simulation
from app.runner.config import config
from app.runner.factory import ServiceFactory
from app.runner.fastapi import CityApi, UvicornServer

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, path: str = "") -> None:
    factory = ServiceFactory(config=config)

    (
        UvicornServer()
        .with_host(host)
        .and_port(port)
        .on_path(path)
        .before_run(factory.world_entities.initialize)
        .run(
            CityApi()
            .with_router(simulation.router)
            .with_router(buildings.router)
            .with_router(people.router)
            .with_websocket_manager(factory.websocket_manager)
            .with_simulation_service(factory.simulation_service)
            .with_buildings_service(factory.buildings_service)
            .with_people_service(factory.people_service)
            .with_snapshot_service(factory.snapshot_service)
            .build()
        )
    )
