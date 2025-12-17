import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import simulation
from app.runner.websocket import ConnectionManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Simulation starting...")
    task = asyncio.create_task(simulation.run_simulation(app.state.manager))
    yield

    print("Simulation stopping...")
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

        app.state.manager = ConnectionManager()

        app.include_router(simulation.router)

        static_dir = Path(__file__).parent.parent.parent / "static"
        if static_dir.exists():
            app.mount(
                "/", StaticFiles(directory=str(static_dir), html=True), name="static"
            )

        return app
