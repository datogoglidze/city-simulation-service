from fastapi import APIRouter, Depends, WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.routers.dependencies import get_manager
from app.runner.websocket import ConnectionManager

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    manager: ConnectionManager = Depends(get_manager),
) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
