from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.routers.dependables import WebSocketManagerDependable
from app.runner.config import config

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    websocket_manager: WebSocketManagerDependable,
) -> None:
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


# HACK: Get grid size from endpoint because static can't use .env properly
@router.get("/config")
def get_config() -> dict[str, int]:
    return {"grid_size": config.GRID_SIZE}
