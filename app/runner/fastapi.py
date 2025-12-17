from dataclasses import dataclass

from fastapi import FastAPI

from app.routers import hello


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
        )

        app.include_router(hello.router)

        return app
