from dataclasses import dataclass, field

from starlette.websockets import WebSocket


@dataclass
class ConnectionManager:
    active_connections: list[WebSocket] = field(default_factory=list)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)
