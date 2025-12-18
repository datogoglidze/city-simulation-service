from functools import cache

from app.core.people import PeopleService
from app.core.simulation import SimulationService
from app.runner.websocket import WebSocketManager


@cache
def get_websocket_manager() -> WebSocketManager:
    return WebSocketManager()


@cache
def get_people_service() -> PeopleService:
    return PeopleService()


@cache
def get_simulation_service() -> SimulationService:
    return SimulationService(
        websocket_manager=get_websocket_manager(),
        people_service=get_people_service(),
    )
