from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.runner.dependencies import (
    SimulationServiceDependable,
    WebSocketManagerDependable,
)

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    websocket_manager: WebSocketManagerDependable,
    simulation: SimulationServiceDependable,
) -> None:
    await websocket_manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
