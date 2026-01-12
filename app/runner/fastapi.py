import asyncio
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import AsyncGenerator

from click import echo
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import people, simulation
from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService
from app.services.simulation import SimulationService
from app.services.snapshot import SnapshotService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    echo("Simulation starting...")

    simulation_task = asyncio.create_task(app.state.simulation.run())
    snapshot_task = asyncio.create_task(app.state.snapshot_service.run_periodic_save())

    yield

    echo("Simulation stopping...")
    simulation_task.cancel()
    snapshot_task.cancel()

    with suppress(asyncio.CancelledError):
        await simulation_task
    with suppress(asyncio.CancelledError):
        await snapshot_task


def create_app(
    websocket: WebSocketManager,
    simulation_service: SimulationService,
    snapshot_service: SnapshotService,
    people_service: PeopleService,
) -> FastAPI:
    app = FastAPI(
        title="City Simulator",
        description="Simulates city behavior",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.state.websocket = websocket
    app.state.simulation = simulation_service
    app.state.snapshot_service = snapshot_service
    app.state.people = people_service

    app.include_router(simulation.router)
    app.include_router(people.router)

    static_dir = Path(__file__).parent.parent.parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app
