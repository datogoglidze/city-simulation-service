from functools import cache

from app.core.people import PeopleService
from app.core.simulation import SimulationService
from app.runner.websocket import ConnectionManager


@cache
def get_manager() -> ConnectionManager:
    return ConnectionManager()


@cache
def get_people_service() -> PeopleService:
    return PeopleService()


@cache
def get_simulation_service() -> SimulationService:
    return SimulationService(
        manager=get_manager(),
        people_service=get_people_service(),
    )
