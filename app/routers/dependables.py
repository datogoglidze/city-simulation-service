from typing import Annotated

from fastapi import Depends, WebSocket
from starlette.requests import Request

from app.services.buildings import BuildingsService
from app.services.people import PeopleService
from app.services.websocket import WebSocketService


def get_people_service(request: Request) -> PeopleService:
    return request.app.state.people  # type: ignore


PeopleServiceDependable = Annotated[PeopleService, Depends(get_people_service)]


def get_buildings_service(request: Request) -> BuildingsService:
    return request.app.state.buildings  # type: ignore


BuildingsServiceDependable = Annotated[BuildingsService, Depends(get_buildings_service)]


def get_websocket_manager(websocket: WebSocket) -> WebSocketService:
    return websocket.app.state.websocket  # type: ignore


WebSocketManagerDependable = Annotated[WebSocketService, Depends(get_websocket_manager)]
