from fastapi import APIRouter, Depends, WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.routers.dependencies import get_websocket_manager
from app.runner.websocket import WebSocketManager

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    websocket_manager: WebSocketManager = Depends(get_websocket_manager),
) -> None:
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
