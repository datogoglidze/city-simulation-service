from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncGenerator, Callable

import uvicorn
from click import echo
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from app.runner.websocket import WebSocketManager
from app.services.locations import LocationsService
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService


@dataclass
class CityApi:
    routes: list[APIRouter] = field(default_factory=list)
    websocket: WebSocketManager = field(init=False)
    simulation_service: SimulationService = field(init=False)
    people_service: PeopleService = field(init=False)
    locations_service: LocationsService = field(init=False)
    snapshot_service: SnapshotService | None = None

    def with_router(self, router: APIRouter) -> CityApi:
        self.routes.append(router)

        return self

    def with_websocket_manager(self, websocket: WebSocketManager) -> CityApi:
        self.websocket = websocket

        return self

    def with_simulation_service(self, simulation_service: SimulationService) -> CityApi:
        self.simulation_service = simulation_service

        return self

    def with_people_service(self, people_service: PeopleService) -> CityApi:
        self.people_service = people_service

        return self

    def with_locations_service(self, locations_service: LocationsService) -> CityApi:
        self.locations_service = locations_service

        return self

    def with_snapshot_service(
        self, snapshot_service: SnapshotService | None
    ) -> CityApi:
        self.snapshot_service = snapshot_service

        return self

    def build(self) -> FastAPI:
        app = FastAPI(
            title="City Simulator",
            description="Simulates city behavior",
            version="0.1.0",
            lifespan=lifespan,
        )

        app.state.websocket = self.websocket
        app.state.simulation = self.simulation_service
        app.state.snapshot_service = self.snapshot_service
        app.state.people = self.people_service
        app.state.locations = self.locations_service

        for router in self.routes:
            app.include_router(router)

        static_dir = Path(__file__).parent.parent.parent / "static"
        if static_dir.exists():
            app.mount(
                "/",
                StaticFiles(directory=str(static_dir), html=True),
                name="static",
            )

        app.swagger_ui_parameters = {"docExpansion": None}

        return app


@dataclass
class UvicornServer:
    host: str = "0.0.0.0"
    port: int = 8000
    path: str = ""

    startup_handlers: list[Callable[[], None]] = field(default_factory=list)

    def with_host(self, value: str) -> UvicornServer:
        self.host = value

        return self

    def and_port(self, value: int | str) -> UvicornServer:
        self.port = int(value)

        return self

    def on_path(self, value: str) -> UvicornServer:
        self.path = value

        return self

    def before_run(self, execute: Callable[[], None]) -> UvicornServer:
        self.startup_handlers.append(execute)

        return self

    def run(self, api: FastAPI) -> None:
        self.on_startup()

        uvicorn.run(
            api,
            host=self.host,
            port=self.port,
            root_path=self.path,
        )

    def on_startup(self) -> None:
        for handler in self.startup_handlers:
            handler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    echo("Simulation starting...")

    simulation_task = asyncio.create_task(app.state.simulation.run())

    snapshot_task = None
    if app.state.snapshot_service:
        snapshot_task = asyncio.create_task(
            app.state.snapshot_service.run_periodic_save()
        )

    yield

    echo("Simulation stopping...")
    simulation_task.cancel()
    if snapshot_task:
        snapshot_task.cancel()

    with suppress(asyncio.CancelledError):
        await simulation_task
    if snapshot_task:
        with suppress(asyncio.CancelledError):
            await snapshot_task
