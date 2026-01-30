from dataclasses import dataclass, field
from typing import Any

from starlette.websockets import WebSocket


@dataclass
class WebSocketService:
    active_connections: list[WebSocket] = field(default_factory=list)

    @property
    def has_active_connections(self) -> bool:
        return bool(self.active_connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, data: list[dict[str, Any]]) -> None:
        for connection in self.active_connections:
            await connection.send_json(data)
