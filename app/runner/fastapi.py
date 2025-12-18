import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncGenerator

from click import echo
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import people, simulation
from app.routers.dependencies import get_simulation_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    echo("Simulation starting...")
    task = asyncio.create_task(get_simulation_service().run())
    yield

    echo("Simulation stopping...")
    task.cancel()


@dataclass
class FastApiConfig:
    title: str = "City Simulator"
    description: str = "Simulates city behavior"
    version: str = "0.1.0"

    def setup(self) -> FastAPI:
        app = FastAPI(
            title=self.title,
            description=self.description,
            version=self.version,
            lifespan=lifespan,
        )

        app.include_router(people.router)
        app.include_router(simulation.router)

        static_dir = Path(__file__).parent.parent.parent / "static"
        if static_dir.exists():
            app.mount(
                "/", StaticFiles(directory=str(static_dir), html=True), name="static"
            )

        return app
