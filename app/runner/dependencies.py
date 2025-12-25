from typing import Annotated

from fastapi import Depends, WebSocket
from starlette.requests import Request

from app.runner.websocket import WebSocketManager
from app.services.people import PeopleService


def get_people_service(request: Request) -> PeopleService:
    return request.app.state.people  # type: ignore


PeopleServiceDependable = Annotated[PeopleService, Depends(get_people_service)]


def get_websocket_manager(websocket: WebSocket) -> WebSocketManager:
    return websocket.app.state.websocket  # type: ignore


WebSocketManagerDependable = Annotated[WebSocketManager, Depends(get_websocket_manager)]
